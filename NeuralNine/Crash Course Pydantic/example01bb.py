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


# =========================
# OpenAI configuration
# =========================

# Create an OpenAI model.
# This configuration is commented out because we are using Ollama.
#
# model = OpenAIChatModel(
#     'openai:gpt-4o',
#     provider=OpenAIProvider(openai_client=client),
# )


# =========================
# Ollama configuration
# =========================

# Create an Ollama model running locally.
# "qwen3:1.7b" is the model we want to use.
# The base URL points to the local Ollama API.
model = OllamaModel(
    "qwen3:1.7b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    )
)


# Create an AI agent using the selected model.
# The system prompt defines the assistant's behavior.
agent = Agent(
    model,
    system_prompt="You are a helpful assistant."
)


# Define the asynchronous main function.
async def main():

    # Start the agent and stream the response progressively.
    # The context manager automatically handles the streaming lifecycle.
    async with agent.run_stream("What is Python ?") as run:

        # Stream the response text as it is generated.
        #
        # delta=True means that only the newly generated part
        # of the response is returned at each iteration.
        #
        # For example, instead of receiving:
        # "Hello"
        # "Hello, how"
        # "Hello, how are"
        #
        # we receive only the new pieces:
        # "Hello"
        # ", how"
        # " are"
        async for chunk in run.stream_text(delta=True):

            # Print each new chunk immediately.
            #
            # end='' prevents print() from adding a new line
            # after every chunk.
            #
            # flush=True forces Python to display the output
            # immediately in the terminal.
            print(chunk, flush=True, end='')


# Run the asynchronous main function when this file
# is executed directly.
if __name__ == "__main__":
    asyncio.run(main())
