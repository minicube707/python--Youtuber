from dataclasses import dataclass

# from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt


# ============================================================
# 1. MODEL CONFIGURATION
# ============================================================

# Name of the model installed and available in Ollama.
MODEL = "qwen3.5:9b"

# ============================================================
# 2. DEFINE THE RUNTIME CONTEXT
# ============================================================

@dataclass
class Context:
    """
    Runtime context passed to the agent.

    The user_role field determines how the assistant
    should formulate its response.
    """

    user_role: str


# ============================================================
# 3. CREATE A DYNAMIC SYSTEM PROMPT
# ============================================================

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """
    Generate a different system prompt depending
    on the user's role.
    """

    # Retrieve the context provided when invoking the agent.
    user_role = request.runtime.context.user_role

    # Base instructions shared by all users.
    base_prompt = ("You are a helpful and very concise assistant.")

    # Change the prompt depending on the user's role.
    match user_role:

        # Expert users receive more technical details.
        case "expert":
            return (f"{base_prompt} Provide detailed technical responses.")

        # Beginner users receive simple explanations.
        case "beginner":
            return (
                f"{base_prompt} Keep your explanations simple and basic.")

        # Children receive explanations using very simple language.
        case "child":
            return (
                f"{base_prompt} Explain everything as if you were literally talking to a five-year-old.")

        # Use the base prompt for unknown roles.
        case _:
            return base_prompt


# ============================================================
# 4. INITIALIZE THE CHAT MODEL
# ============================================================

# Create a ChatOllama instance.
# This object is used to communicate with the local
# language model through Ollama.
model = ChatOllama(
    model=MODEL,

    # A temperature of 0 makes the model's responses
    # more deterministic and less random.
    temperature=0
)


# ============================================================
# 5. ALTERNATIVE MODEL CONFIGURATION
# ============================================================

# Another option is to use LangChain's init_chat_model().
#
# This example is commented out because we are currently
# using ChatOllama with a local model.
#
# model = init_chat_model(
#     model="gpt-4.1-mini",
#     temperature=0.1
# )


# ============================================================
# 6. CREATE THE AGENT
# ============================================================

# Middleware classes and decorators used to dynamically
# modify the model's prompt at runtime.
# Create the LangChain agent with a dynamic prompt middleware
# that executes at runtime to generate the appropriate system
# prompt based on the user's role.
# context_schema defines the structure of the runtime context.

agent = create_agent(
    model=model,
    middleware=[user_role_prompt],
    context_schema=Context
)


# ============================================================
# 7. INVOKE THE AGENT
# ============================================================

# Send a question to the agent.
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Explain PCA.",
            }
        ]
    },

    # Provide the runtime context.
    #
    # Because the role is "beginner", the dynamic prompt
    # will instruct the model to provide a detailed
    # technical explanation.
    context=Context(
        user_role="beginner"
    ),
)


# ============================================================
# 8. DISPLAY RAW RESPONSE
# ============================================================

# Print the complete response returned by the agent.
# This can contain all the messages exchanged during execution.
print("\n" + 60 * "=")
print("Raw Response:")
print(response)


# ============================================================
# 9. DISPLAY CLEAN RESPONSE
# ============================================================

# Print only the content of the agent's final message.
# The last message usually contains the final answer
# intended for the user.
print("\nClean Response:")
print(response["messages"][-1].content)