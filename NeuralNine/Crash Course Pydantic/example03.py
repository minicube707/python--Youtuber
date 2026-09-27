import asyncio
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic import BaseModel

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
#
# The system prompt defines the general behavior of the assistant.
agent = Agent(
    model,
    system_prompt=
        "You are a helpful assistant. "
        "You always respond with a structured output for people.",
)


# Define the asynchronous main function.
async def main():

    # Send the first message to the agent.
    #
    # The agent generates a response and stores the messages
    # exchanged during this interaction.
    response = await agent.run("What is Python ?")

    # Print the first response.
    print(response.output)


    # Send a second message to the same agent.
    #
    # "message_history=response.all_messages()" passes the
    # previous conversation history to the agent.
    #
    # This allows the model to understand that "it" refers
    # to Python from the previous conversation.
    response = await agent.run(
        "And when was it released ?",
        message_history=response.all_messages()
    )

    # Print the second response.
    print(response.output)


# Run the asynchronous main function when this file
# is executed directly.
if __name__ == "__main__":
    asyncio.run(main())
