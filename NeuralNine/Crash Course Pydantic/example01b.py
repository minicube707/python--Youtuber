import asyncio
from dotenv import load_dotenv

from pydantic_ai import Agent

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider


# Load environment variables from the .env file.
# This can be useful for storing API keys and other configuration values.
load_dotenv()


# =========================
# OpenAI configuration
# =========================

# Create an OpenAI model.
# This configuration is commented out because we are using Ollama below.
#
# model = OpenAIChatModel(
#     'openai:gpt-4o',
#     provider=OpenAIProvider(openai_client=client),
# )


# =========================
# Ollama configuration
# =========================

# Create an Ollama model running locally.
# "qwen3:1.7b" is the name of the model we want to use.
# The base URL points to the local Ollama API.
model = OllamaModel(
    "qwen3:1.7b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    )
)


# Create an AI agent using the selected model.
# The system prompt defines the assistant's general behavior.
agent = Agent(
    model,
    system_prompt="You are a helpful assistant.")


# Define the asynchronous main function.
async def main():

    # Start the agent and stream the response progressively.
    # Unlike agent.run(), run_stream() does not wait for the
    # entire response before returning the result.
    async with agent.run_stream("What is Python ?") as run:

        # Read the generated text as it becomes available.
        # Each iteration contains a new part of the response.
        async for output in run.stream_text():

            # Print each part immediately to the console.
            # end="" prevents Python from adding a new line
            # after every streamed chunk.
            print(output, end="", flush=True)


# This condition ensures that main() is only executed
# when this file is run directly.
if __name__ == "__main__":
    asyncio.run(main())
