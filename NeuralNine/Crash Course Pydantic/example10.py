import asyncio
from dotenv import load_dotenv

from pydantic_ai import Agent, WebSearchTool
from pydantic_ai.capabilities import NativeTool

from pydantic_ai.models.openai import OpenAIResponsesModel

load_dotenv()

# OpenAI model configuration
model = OpenAIResponsesModel('openai:gpt-4o')


# Create the AI agent and enable native web search
agent = Agent(
    model,
    system_prompt="You are a helpful assistant.",
    capabilities=[NativeTool(WebSearchTool())]
)


async def main():
    # Ask the agent to search the web for the latest NeuralNine video
    response = await agent.run("What is the latest video from NeuralNine?")
    print(response.output)


if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
