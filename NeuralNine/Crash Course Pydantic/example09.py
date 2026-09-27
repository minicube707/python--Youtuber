import asyncio
from dotenv import load_dotenv

from pydantic_ai import Agent

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

load_dotenv()

# OpenAI model configuration
# model = OpenAIChatModel(
#     'openai:gpt-4o',
#     provider=OpenAIProvider(openai_client=client),
# )

# Ollama model configuration
model = OllamaModel(
    "qwen3:1.7b",
    provider=OllamaProvider(base_url="http://localhost:11434/v1")
)

# Create the AI agent with a system prompt,
# a timeout for tools, and a retry limit
agent = Agent(
    model,
    system_prompt="You are a helpful assistant.",
    tool_timeout=5,
    retries=5
)


# Define a tool that simulates a slow operation
@agent.tool_plain
async def get_favorite_color_slow() -> str:
    await asyncio.sleep(10)
    return 'Blue'


async def main():
    # Ask the agent to find out the user's favorite color
    response = await agent.run("What is my favorite color?")
    print(response.output)


if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
