import asyncio
from dotenv import load_dotenv

from pydantic_ai import Agent, RunContext

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
# "qwen3:4b" is the model we want to use.
# The base URL points to the local Ollama API.
model = OllamaModel(
    "qwen3:4b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    )
)


# Create a roulette agent.
#
# "deps_type=int" defines the type of the dependency
# that will be passed to the agent at runtime.
#
# "output_type=bool" tells Pydantic AI that the final
# response should be a boolean value: True or False.
roulette_agent = Agent(
    model,
    deps_type=int,
    output_type=bool,
    system_prompt=
        "You are a roulette assistant. "
        "You can process number guesses from users."
)


# Register a tool that has access to the agent's runtime context.
#
# Unlike @agent.tool_plain, @agent.tool allows us to use
# RunContext to access dependencies and other runtime information.
@roulette_agent.tool
async def guess_number(
    ctx: RunContext[int],
    guessed_number: int
) -> str:
    """Check whether the guessed roulette number is correct."""

    # Compare the user's guess with the correct number.
    #
    # "ctx.deps" contains the dependency passed to the agent
    # when agent.run() is called.
    return "won" if guessed_number == ctx.deps else "lost"


# Define the asynchronous main function.
async def main():

    # This represents the correct roulette number.
    #
    # In a real application, this value could come from
    # a database, an API, or another external service.
    correct_number = 17


    # Run the agent with the user's message.
    #
    # "deps=correct_number" injects the value 17 into the
    # agent's runtime context.
    #
    # The model can decide to call guess_number() with
    # the number mentioned by the user.
    response = await roulette_agent.run(
        "I want to put my money on eighteen!",
        deps=correct_number
    )


    # Print the final structured output.
    #
    # Because output_type=bool, response.output should be
    # a Python boolean: True or False.
    print(response.output)


# Run the asynchronous main function when this file
# is executed directly.
if __name__ == "__main__":
    asyncio.run(main())
