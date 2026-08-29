import requests
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver


# ============================================================
# 1. MODEL CONFIGURATION
# ============================================================

MODEL = "gemma4:12b"


# ============================================================
# 2. DATACLASSES
# ============================================================

@dataclass
class Context:
    user_id: str


@dataclass
class ResponseFormat:
    summary: str
    temperature_celsius: float
    temperature_fahrenheit: float
    humidity: float


# ============================================================
# 3. TOOLS
# ============================================================

@tool(
    "get_weather",
    description="Return current weather information for a given city.",
)
def get_weather(city: str) -> dict:
    """Retrieve current weather information for a city."""

    response = requests.get(
        f"https://wttr.in/{city}?format=j1",
        timeout=10,
    )

    # Raise an exception if the HTTP request failed.
    response.raise_for_status()

    # Convert the response to a Python dictionary.
    return response.json()


@tool(
    "locate_user",
    description="Look up the user's city based on the user ID in the context.",
)
def locate_user(runtime: ToolRuntime[Context]) -> str:
    """Return the city associated with the current user."""

    match runtime.context.user_id:
        case "ABC123":
            return "Vienna"
        case "XYZ456":
            return "London"
        case "HJKL111":
            return "Paris"
        case _:
            return "Unknown"


# ============================================================
# 4. LANGUAGE MODEL
# ============================================================

model = ChatOllama(
    model=MODEL,
    temperature=0.3,
)


# ============================================================
# 5. CHECKPOINTER
# ============================================================

checkpointer = InMemorySaver()


# ============================================================
# 6. AGENT CONFIGURATION
# ============================================================

agent = create_agent(
    model=model,
    tools=[
        get_weather,
        locate_user,
    ],
    system_prompt=(
        "You are a helpful weather assistant. "
        "You are humorous and always include a small joke "
        "while remaining useful and accurate. "
        "If the user asks for the weather without specifying a city, "
        "use the locate_user tool to determine their city, "
        "then use get_weather to retrieve the weather."
    ),
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer,
)


# ============================================================
# 7. AGENT EXECUTION
# ============================================================

config = {
    "configurable": {
        "thread_id": "1",
    }
}

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the weather?",
            }
        ]
    },
    config=config,
    context=Context(user_id="ABC123"),
)


# ============================================================
# 8. DISPLAY RAW RESPONSE
# ============================================================

print("\n" + 60 * "=")
print("Raw Response:")
print(response)


# ============================================================
# 9. DISPLAY STRUCTURED RESPONSE
# ============================================================

structured_response = response["structured_response"]

print("\nClean Response:")
print(response['messages'][-1].content)

print("\nClean Structured Response:")
print(structured_response)

if structured_response is not None:

    print("\nClean Response Summary:")
    print(structured_response.summary)

    print("\nClean Response Temperature:")
    print(structured_response.temperature_celsius)

    print("\nClean Response Temperature (°F):")
    print(structured_response.temperature_fahrenheit)

    print("\nClean Response Humidity:")
    print(structured_response.humidity)

else:
    print("No structured response was generated.")