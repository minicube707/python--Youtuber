import asyncio
from dotenv import load_dotenv

from pydantic_ai import Agent

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider


# Load environment variables from the .env file.
# This is useful for storing configuration values such as API keys.
load_dotenv()


# Pydantic AI documentation:
# https://pydantic.dev/docs/validation/dev/get-started/


# =========================
# OpenAI configuration
# =========================

# Create an OpenAI model.
# This section is commented out because we are currently using Ollama.
#
# model = OpenAIChatModel(
#     'openai:gpt-4o',
#     provider=OpenAIProvider(openai_client=client),
# )


# =========================
# Ollama configuration
# =========================

# Create an Ollama model running locally.
# "qwen3:1.7b" is the name of the model installed in Ollama.
# The base URL points to the local Ollama server.
model = OllamaModel(
    "qwen3:1.7b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    )
)


# Create a Pydantic AI agent using the selected model.
# The system prompt defines the assistant's general behavior.
agent = Agent(
    model,
    system_prompt=
        "You are a helpful assistant. "
        "You always respond with a structured output for people."
)


# Define the asynchronous main function.
# The "async" keyword allows us to use "await" inside the function.
async def main():

    # Send a prompt to the AI agent and wait for its response.
    response = await agent.run("What is Python ?")

    # Print the generated response to the console.
    print(response.output)


# This condition ensures that main() is only executed
# when this file is run directly, not when it is imported.
if __name__ == "__main__":
    asyncio.run(main())
