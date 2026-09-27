import asyncio
from dotenv import load_dotenv

from pydantic_ai import Agent, CodeExecutionTool
from pydantic_ai.capabilities import NativeTool

from pydantic_ai.models.openai import OpenAIResponsesModel

load_dotenv()

# ============================================================
# OpenAI configuration
# ============================================================

model = OpenAIResponsesModel('openai:gpt-4o')


# ============================================================
# Agent configuration
# ============================================================

agent = Agent(
    model,
    system_prompt="You are a helpful assistant.",
    capabilities=[NativeTool(CodeExecutionTool())]
)


# ============================================================
# Main function
# ============================================================

async def main():
    # Ask the agent to calculate the factorial of 24
    response = await agent.run("What is the factorial of 24?")
    print(response.output)


if __name__ == "__main__":
    # Start the asynchronous application
    asyncio.run(main())
