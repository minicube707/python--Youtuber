from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools import search_tool, save_to_txt, wiki_tool

MODEL = "qwen3.5:9b"

# ============================================================
# 1. MODEL
# ============================================================

# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
# llm = ChatOpenAI(model="gpt-5.4-mini")
llm = ChatOllama(model=MODEL, temperature=0)


# ============================================================
# 2. TOOLS
# ============================================================

tools = [
    search_tool,
    save_to_txt,
    wiki_tool
]


# ============================================================
# 3. DISPLAY AVAILABLE TOOLS
# ============================================================

print("\n" + "=" * 60)
print("AVAILABLE TOOLS")
print("=" * 60)

for tool in tools:
    print(f"\n🔧 Tool: {tool.name}")
    print(f"   Description: {tool.description}")

    if hasattr(tool, "args_schema") and tool.args_schema:
        print(f"   Schema: {tool.args_schema}")


# ============================================================
# 4. CREATE AGENT
# ============================================================

agent = create_agent(
    model=llm,
    tools=tools,
)


# ============================================================
# 5. USER QUERY
# ============================================================

query = input("\nWhat can I help you research?\n> ")


print("\n" + "=" * 60)
print("USER QUERY")
print("=" * 60)
print(query)


# ============================================================
# 6. RUN AGENT
# ============================================================

print("\n" + "=" * 60)
print("AGENT EXECUTION")
print("=" * 60)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": query,
            }
        ]
    }
)


# ============================================================
# 7. INSPECT ALL MESSAGES
# ============================================================

print("\n" + "=" * 60)
print("MESSAGES")
print("=" * 60)

for i, message in enumerate(result["messages"], start=1):

    print(f"\n--- Message {i} ---")

    print(f"Type: {message.__class__.__name__}")

    # --------------------------------------------------------
    # Message content
    # --------------------------------------------------------

    if hasattr(message, "content"):
        if message.content:
            print("\nContent:")
            print(message.content)

    # --------------------------------------------------------
    # Tool calls made by the LLM
    # --------------------------------------------------------

    if hasattr(message, "tool_calls") and message.tool_calls:

        print("\n🤖 LLM TOOL SELECTION:")

        for tool_call in message.tool_calls:

            print(f"\n   Tool selected: {tool_call['name']}")

            print("   Arguments:")
            print(f"   {tool_call['args']}")

            print(f"   Tool call ID: {tool_call['id']}")

    # --------------------------------------------------------
    # Tool result
    # --------------------------------------------------------

    if message.__class__.__name__ == "ToolMessage":

        print("\n🔧 TOOL RESULT:")
        print(message.content)


# ============================================================
# 8. FINAL ANSWER
# ============================================================

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

for message in reversed(result["messages"]):

    if message.__class__.__name__ == "AIMessage":

        # Ignore AI messages that only contain tool calls
        if message.content:
            print(message.content)
            break