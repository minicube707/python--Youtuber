import asyncio
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.capabilities import MCP

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

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
    provider=OllamaProvider(base_url="http://localhost:11434/v1")
)


# ============================================================
# MCP server configuration
# ============================================================

server = MCP('http://localhost:8000/mcp')


# ============================================================
# Agent configuration
# ============================================================

agent = Agent(
    model,
    capabilities=[server]
)


# ============================================================
# Main function
# ============================================================

async def main():
    # Ask the agent to retrieve the user's favorite color
    result = await agent.run('What is my favorite color?')
    print(result.output)


# Start the asynchronous application
asyncio.run(main())
