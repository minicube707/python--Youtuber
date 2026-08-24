import asyncio
from ollama import chat
from fastmcp import Client

MODEL = "qwen3.5:0.8b"
SERVER = "server.py"


# Test the connexion and list the tools
# async def main():
#     async with Client(SERVER) as client:
#         tools = await client.list_tools()

#         print("Outils MCP disponibles :")
#         for tool in tools:
#             print(f"- {tool.name}: {tool.description}")


# Ollama use the MCP tools
async def main():
    async with Client(SERVER) as client:
        mcp_tools = await client.list_tools()

        tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema,
                },
            }
            for tool in mcp_tools
        ]

        messages = [
            {
                "role": "user",
                "content": input("What would you ask ?\n"), #"Ajoute une note disant : acheter du lait"
            }
        ]

        while True:
            response = chat(
                model=MODEL,
                messages=messages,
                tools=tools,
            )

            message = response["message"]
            messages.append(message)

            if not message.get("tool_calls"):
                print(message["content"])
                break

            for call in message["tool_calls"]:
                name = call["function"]["name"]
                arguments = call["function"]["arguments"]

                result = await client.call_tool(
                    name,
                    arguments,
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_name": name,
                        "content": str(result.content),
                    }
                )


if __name__ == "__main__":
    asyncio.run(main())
