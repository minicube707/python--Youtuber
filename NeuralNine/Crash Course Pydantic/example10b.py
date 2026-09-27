import asyncio
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.capabilities import WebSearch

from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider


load_dotenv()

# ============================================================
# OpenAI configuration
# ============================================================

# model = OpenAIChatModel(
#     'openai:gpt-4o',
#     provider=OpenAIProvider(openai_client=client),
# )

# ============================================================
# Ollama configuration
# ============================================================

model = OllamaModel(
    "qwen3:1.7b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)

# ============================================================
# Web search configuration
# ============================================================

web_search = WebSearch(local="duckduckgo")


# ============================================================
# Agent configuration
# ============================================================

agent = Agent(
    model=model,
    system_prompt=
    """
        You are a helpful assistant.

        When the user asks for recent or current information,
        use the web search tool.

        Always use the information returned by the web search
        to formulate your answer.
    """,
    capabilities=[web_search],
)


# ============================================================
# Main function
# ============================================================

async def main():
    # Run the agent with a query requiring recent information
    response = await agent.run("What is the latest video from NeuralNine?")
    
    # Display the agent's final response
    print("=== OUTPUT ===")
    print(response.output)

    # Display all messages exchanged during the agent run
    print("\n=== MESSAGES ===")
    for message in response.all_messages():
        print(message)
        print("-" * 80)


if __name__ == "__main__":
    # Start the asynchronous application
    asyncio.run(main())
