import asyncio

import ollama
from fastmcp import Client

MODEL = "qwen3.5:0.8b"                  # Change to your model on ollama
SERVER = "server_maths.py"              # Change between "server_maths.py", "server_notes.py" and "server_weather.py


# ---------------------------------------------------------------------------
# TOOLS
# ---------------------------------------------------------------------------

async def get_ollama_tools(mcp: Client) -> list:
    """
    Fetch all tools exposed by the MCP client and convert them into
    the function-calling format expected by Ollama.

    Args:
        mcp: The MCP client used to retrieve the available tools.

    Returns:
        A list of dictionaries describing the available tools in
        Ollama's function definition format.
    """

    tools = await mcp.list_tools()

    ollama_tools = []

    print("\nTools:")
    for tool in tools:
        print("Tool found:", tool.name)

        ollama_tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
        )

    return ollama_tools


# ---------------------------------------------------------------------------
# RESOURCES
# Resources are NOT callable functions: they're data identified by a URI.
# We just list them, and read their content on demand to inject into the
# conversation as context (e.g. a system/user message).
# ---------------------------------------------------------------------------

async def get_mcp_resources(mcp: Client) -> list:
    """
    List all resources exposed by the MCP server.

    Args:
        mcp: The MCP client used to retrieve the available resources.

    Returns:
        A list of resource descriptors (uri, name, description, mimeType).
    """

    resources = await mcp.list_resources()

    resource_list = []

    print("\nResource:")
    for resource in resources:
        print("Resource found:", resource.uri, "-", resource.name)

        resource_list.append(
            {
                "uri": str(resource.uri),
                "name": resource.name,
                "description": resource.description,
                "mime_type": resource.mimeType,
            }
        )

    return resource_list


async def read_mcp_resource(mcp: Client, uri: str) -> str:
    """
    Read the content of a given resource and return it as plain text.

    Args:
        mcp: The MCP client used to read the resource.
        uri: The URI of the resource to read.

    Returns:
        The concatenated text content of the resource.
    """

    result = await mcp.read_resource(uri)

    texts = []
    for content in result:
        # Resource contents can be text or binary (blob); we only
        # concatenate the text ones here.
        text = getattr(content, "text", None)
        if text is not None:
            texts.append(text)

    return "\n".join(texts)


# ---------------------------------------------------------------------------
# PROMPTS
# Prompts are server-defined conversation templates. list_prompts() gives
# their name/arguments, get_prompt() returns the ready-to-use messages.
# ---------------------------------------------------------------------------

async def get_mcp_prompts(mcp: Client) -> list:
    """
    List all prompt templates exposed by the MCP server.

    Args:
        mcp: The MCP client used to retrieve the available prompts.

    Returns:
        A list of prompt descriptors (name, description, arguments).
    """

    prompts = await mcp.list_prompts()

    prompt_list = []

    print("\nPrompt:")
    for prompt in prompts:
        print("Prompt found:", prompt.name)

        prompt_list.append(
            {
                "name": prompt.name,
                "description": prompt.description,
                "arguments": prompt.arguments,
            }
        )

    return prompt_list


async def build_messages_from_prompt(mcp: Client, name: str, arguments: dict) -> list:
    """
    Fetch a prompt template from the MCP server and convert it into
    Ollama-compatible chat messages.

    Args:
        mcp: The MCP client used to fetch the prompt.
        name: The name of the prompt to fetch.
        arguments: The arguments to fill in the prompt template.

    Returns:
        A list of chat messages ready to send to Ollama.
    """

    result = await mcp.get_prompt(name, arguments)

    messages = []
    for msg in result.messages:
        # msg.content can be text or embedded resource/image content.
        content = getattr(msg.content, "text", None) or str(msg.content)
        messages.append({"role": msg.role, "content": content})

    return messages


# ---------------------------------------------------------------------------
# OLLAMA CALL
# ---------------------------------------------------------------------------

def ask_model(messages: list, tools: list | None = None) -> dict:
    """
    Send a conversation to the Ollama model and return its response.

    Args:
        messages: The conversation history formatted as a list of chat messages.
        tools: An optional list of tool definitions available for function
            calling by the model.

    Returns:
        The response returned by the Ollama chat API, including any generated
        message or requested tool calls.
    """
    return ollama.chat(
        model=MODEL,
        messages=messages,
        tools=tools,
    )


async def execute_tool_calls(mcp: Client, message: dict, messages: list) -> None:
    """
    Execute all tool calls requested by the model and append their
    results to the conversation history.

    Args:
        mcp: The MCP client used to execute the requested tools.
        message: The assistant message containing one or more tool calls.
        messages: The conversation history, updated in place with the
            assistant tool call and each corresponding tool response.

    Returns:
        None.
    """

    for call in message["tool_calls"]:
        tool_name = call["function"]["name"]
        arguments = call["function"]["arguments"]

        print("Call tool:", tool_name)
        result = await mcp.call_tool(tool_name, arguments)

        # Save the assistant tool call
        messages.append(message)

        # Save the tool output
        messages.append(
            {
                "role": "tool",
                "content": str(result),
            }
        )


# ---------------------------------------------------------------------------
# CLI HELPERS
# ---------------------------------------------------------------------------

def choose_prompt(prompts: list) -> dict | None:
    """
    Ask the user whether they want to start the conversation from a
    server-defined prompt template.

    Args:
        prompts: The list of prompt descriptors available.

    Returns:
        The chosen prompt descriptor, or None if the user skips this step.
    """

    if not prompts:
        return None

    print("\nAvailable prompts:")
    for i, p in enumerate(prompts):
        print(f"  [{i}] {p['name']}")
    print("  [n] None, I'll type my own request")

    choice = input("\nUse a prompt? ").strip().lower()
    if choice == "n" or choice == "":
        return None

    try:
        return prompts[int(choice)]
    except (ValueError, IndexError):
        print("Invalid choice, ignoring.")
        return None


def choose_resource(resources: list) -> str | None:
    """
    Ask the user whether they want to attach a resource's content to
    the conversation as extra context.

    Args:
        resources: The list of resource descriptors available.

    Returns:
        The URI of the chosen resource, or None if the user skips this step.
    """

    if not resources:
        return None

    print("\nAvailable resources:")
    for i, r in enumerate(resources):
        print(f"  [{i}] {r['uri']} - {r['name']}")
    print("  [n] None")

    choice = input("\nAttach a resource as context? ").strip().lower()
    if choice == "n" or choice == "":
        return None

    try:
        return resources[int(choice)]["uri"]
    except (ValueError, IndexError):
        print("Invalid choice, ignoring.")
        return None


# ---------------------------------------------------------------------------
# MESSAGE BUILDING
# ---------------------------------------------------------------------------
 
async def build_resource_context_message(mcp: Client, resources: list) -> dict | None:
    """
    Let the user optionally pick a resource and turn its content into a
    single context message.
 
    Args:
        mcp: The MCP client used to read the chosen resource.
        resources: The list of resource descriptors available.
 
    Returns:
        A chat message containing the resource content, or None if the
        user chose not to attach any resource.
    """
 
    resource_uri = choose_resource(resources)
    if resource_uri is None:
        return None
 
    content = await read_mcp_resource(mcp, resource_uri)
 
    return {
        "role": "user",
        "content": f"Context from resource '{resource_uri}':\n{content}",
    }
 
 
async def ask_prompt_arguments(prompt: dict) -> dict:
    """
    Ask the user to provide a value for each argument required by a
    prompt template.
 
    Args:
        prompt: The chosen prompt descriptor.
 
    Returns:
        A dictionary mapping argument names to the values entered by
        the user.
    """
 
    prompt_args = {}
    for arg in prompt.get("arguments") or []:
        value = input(f"  Value for '{arg.name}': ")
        prompt_args[arg.name] = value
 
    return prompt_args
 
 
async def build_prompt_messages(mcp: Client, prompts: list) -> list | None:
    """
    Let the user optionally pick a server-defined prompt template and
    turn it into ready-to-use chat messages.
 
    Args:
        mcp: The MCP client used to fetch the chosen prompt.
        prompts: The list of prompt descriptors available.
 
    Returns:
        A list of chat messages built from the prompt, or None if the
        user chose not to use any prompt.
    """
 
    chosen_prompt = choose_prompt(prompts)
    if chosen_prompt is None:
        return None
 
    prompt_args = await ask_prompt_arguments(chosen_prompt)
 
    return await build_messages_from_prompt(mcp, chosen_prompt["name"], prompt_args)
 
 
def ask_free_text_message() -> dict:
    """
    Ask the user to type a free-text request.
 
    Returns:
        A chat message containing the user's request.
    """
 
    user_input = input("\nEnter a request:\n")
    print("")
    return {"role": "user", "content": user_input}
 
 
async def build_initial_messages(mcp: Client, resources: list, prompts: list) -> list:
    """
    Build the conversation's starting messages: an optional resource
    context, then either a chosen prompt template or a free-text request.
 
    Args:
        mcp: The MCP client used to read resources and fetch prompts.
        resources: The list of resource descriptors available.
        prompts: The list of prompt descriptors available.
 
    Returns:
        The list of chat messages to start the conversation with.
    """
 
    messages = []
 
    resource_message = await build_resource_context_message(mcp, resources)
    if resource_message is not None:
        messages.append(resource_message)
 
    prompt_messages = await build_prompt_messages(mcp, prompts)
    if prompt_messages is not None:
        messages.extend(prompt_messages)
    else:
        messages.append(ask_free_text_message())
 
    return messages
 
 
# ---------------------------------------------------------------------------
# RESPONSE HANDLING
# ---------------------------------------------------------------------------
 
async def get_final_answer(mcp: Client, messages: list, ollama_tools: list) -> str:
    """
    Send the conversation to the model, execute any requested tool
    calls, and return the final textual answer.
 
    Args:
        mcp: The MCP client used to execute tool calls if needed.
        messages: The conversation history to send to the model.
        ollama_tools: The tool definitions available to the model.
 
    Returns:
        The final textual answer generated by the model.
    """
 
    response = ask_model(messages, ollama_tools)
    message = response["message"]
 
    if message.get("tool_calls"):
        await execute_tool_calls(mcp, message, messages)
        final_response = ask_model(messages)
        return final_response["message"]["content"]
 
    return message["content"]
 
 
# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
 
# Main application workflow.
# 1. Connect to the MCP server.
# 2. Retrieve the available tools, resources and prompts.
# 3. Let the user pick a prompt template and/or a resource to attach.
# 4. Ask the language model.
# 5. Execute tool calls if needed.
# 6. Ask the model again to generate the final response.
async def main():
 
    # Create a connection to the MCP server.
    # The 'mcp' object is used to list and execute available tools,
    # read resources, and fetch prompt templates.
    async with Client(SERVER) as mcp:
 
        # List of tools converted to the format expected by Ollama.
        ollama_tools = await get_ollama_tools(mcp)
 
        # List of resources and prompts exposed by the server.
        resources = await get_mcp_resources(mcp)
        prompts = await get_mcp_prompts(mcp)
 
        # Build the starting messages (resource context + prompt/free text).
        messages = await build_initial_messages(mcp, resources, prompts)
 
        # Get the model's final answer, handling tool calls if needed.
        answer = await get_final_answer(mcp, messages, ollama_tools)
 
        print("\nAnswer:")
        print(answer)
 


if __name__ == "__main__":
    asyncio.run(main())