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


# =========================
# Agents using instructions
# =========================

# Create an agent with dynamic instructions.
#
# The instructions are added to the conversation when the agent
# is run and can be useful for providing additional context or
# instructions for a specific execution.
agent1 = Agent(
    model,
    instructions=
        "If asked 'what is your favorite color', "
        "answer exactly BLUE. Otherwise answer normally"
)


agent2 = Agent(
    model,
    instructions=
        "If asked 'what is your favorite color', "
        "answer exactly RED. Otherwise answer normally"
)


# =========================
# Agents using system prompts
# =========================

# Create an agent with a system prompt.
#
# The system prompt defines the agent's general behavior
# and is part of the agent's system-level configuration.
agent3 = Agent(
    model,
    system_prompt=
        "If asked 'what is your favorite color', "
        "answer exactly BLUE. Otherwise answer normally"
)


agent4 = Agent(
    model,
    system_prompt=
        "If asked 'what is your favorite color', "
        "answer exactly RED. Otherwise answer normally"
)


# Define the asynchronous main function.
async def main():

    # =========================
    # Test instructions
    # =========================

    # First, ask agent1 an unrelated question.
    #
    # We keep the resulting conversation history so it can
    # be passed to another agent.
    result = await agent1.run("What 2 + 2 ?")

    history = result.all_messages()


    # Run agent2 using the conversation history created by agent1.
    #
    # This allows us to test how the second agent behaves when
    # it receives a previous conversation from another agent.
    result = await agent2.run(
        "What is your favorite color ?",
        message_history=history
    )

    print(result.output)


    # =========================
    # Test system prompts
    # =========================

    # Start a new conversation with agent3.
    #
    # agent3 has a system prompt that tells it to answer BLUE.
    result = await agent3.run("What 2 + 2 ?")

    history = result.all_messages()


    # Run agent4 using the conversation history created by agent3.
    #
    # agent4 has a system prompt that tells it to answer RED.
    result = await agent4.run(
        "What is your favorite color ?",
        message_history=history
    )

    print(result.output)


# Run the asynchronous main function when this file
# is executed directly.
if __name__ == "__main__":
    asyncio.run(main())
