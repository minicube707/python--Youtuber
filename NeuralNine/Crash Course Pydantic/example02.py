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
# "qwen3.5:0.8b" is the model we want to use.
# The base URL points to the local Ollama API.
model = OllamaModel(
    "qwen3.5:0.8b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    )
)


# Define the expected structure of the AI response.
#
# Pydantic will validate that the generated output contains:
# - a "name" field containing a string
# - an "age" field containing an integer
# - a "job" field containing a string
class Person(BaseModel):
    name: str
    age: int
    job: str


# Create the AI agent using the selected model.
#
# The "system_prompt" gives instructions about the assistant's behavior.
#
# "output_type=Person" tells Pydantic AI that the response
# must follow the structure defined by the Person model.
agent = Agent(
    model,
    system_prompt=
        "You are a helpful assistant. "
        "You always respond with a structured output for people.",
    output_type=Person
)


# Define the asynchronous main function.
async def main():

    # Send information about a person to the AI agent.
    #
    # The model should extract the relevant information
    # and return it using the Person structure.
    response = await agent.run(
        "Mike is a 20 year old plumber."
    )

    # Display the complete response object.
    # The "=" inside the f-string also displays the variable name.
    print(f"{response.output=}")

    # Display the Python type of the generated output.
    # This should be <class '__main__.Person'>.
    print(f"{type(response.output)=}")


# Run the asynchronous main function when this file
# is executed directly.
if __name__ == "__main__":
    asyncio.run(main())
