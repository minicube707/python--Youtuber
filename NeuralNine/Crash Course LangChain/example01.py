import requests

# from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# ============================================================
# 1. MODEL CONFIGURATION
# ============================================================

# Define the Ollama model that will be used by the agent.
MODEL = "qwen3.5:9b"


# ============================================================
# 2. WEATHER TOOL
# ============================================================

# Create a tool that allows the agent to retrieve weather information.
# The tool takes a city name as input and returns weather data as JSON.
@tool(
    'get_weather',
    description="Return weather information for a given city",
    return_direct=False
)
def get_weather(city: str):
    # Send a request to wttr.in to get the current weather information.
    response = requests.get(f"https://wttr.in/{city}?format=j1")

    # Convert the HTTP response into a Python dictionary.
    return response.json()


# ============================================================
# 3. LANGUAGE MODEL
# ============================================================

# Initialize the language model using Ollama.
model = ChatOllama(model=MODEL, temperature=0)


# ============================================================
# 4. ALTERNATIVE MODEL CONFIGURATION
# ============================================================

# Another way to initialize a chat model is by using
# LangChain's init_chat_model function.
#
# In this example, it is commented out because we are
# currently using ChatOllama with a local model.
#
# from langchain.chat_models import init_chat_model
#
# model = init_chat_model(
#     model='gpt-4.1-mini',
#     temperature=0.1
# )

# ============================================================
# 5. AGENT CONFIGURATION
# ============================================================

# Create the LangChain agent.
# The agent can use the get_weather tool when it needs weather information.
agent = create_agent(
    model=model,
    tools=[get_weather],

    # Define the agent's behavior and personality.
    # The agent should be helpful, humorous, and make jokes.
    system_prompt=(
        "You are a helpful weather assistant, "
        "who always cracks jokes and is humorous while remaining helpful"
    )
)


# ============================================================
# 6. AGENT EXECUTION
# ============================================================

# Send a user message to the agent.
# The agent will decide whether it needs to call the weather tool
# before generating its final answer.
response = agent.invoke({
    'messages': [
        {
            'role': 'user',
            'content': 'What is the weather like in Vienna ?'
        }
    ]
})


# ============================================================
# 7. DISPLAY RAW RESPONSE
# ============================================================

# Print the complete response returned by the agent.
# This can contain all the messages exchanged during the execution.
print("\n" + 60 * "=")
print("Raw Response:")
print(response)


# ============================================================
# 8. DISPLAY CLEAN RESPONSE
# ============================================================

# Print only the content of the agent's final message.
# The last message usually contains the final answer intended for the user.
print("\nClean Response:")
print(response['messages'][-1].content)