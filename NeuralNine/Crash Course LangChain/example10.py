import time

from langchain.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, AgentState
# from langchain.chat_models import init_chat_model


# ============================================================
# 1. MODEL CONFIGURATION
# ============================================================

# Name of the model installed and available in Ollama.
MODEL = "qwen3.5:9b"

# ============================================================
# 2. CUSTOM MIDDLEWARE WITH LIFECYCLE HOOKS
# ============================================================

class HooksDemo(AgentMiddleware):
    """
    Custom middleware demonstrating the main agent lifecycle hooks.

    The hooks allow us to execute custom code:
    - Before the agent starts
    - Before the model is called
    - After the model responds
    - After the agent finishes
    """

    def __init__(self):
        # Initialize the parent AgentMiddleware class.
        super().__init__()

        # Store the timestamp at which the agent starts.
        self.start_time = 0.0

    # --------------------------------------------------------
    # 2.1 BEFORE AGENT
    # --------------------------------------------------------

    def before_agent(self, state: AgentState, runtime):
        """
        Called before the agent starts processing the request.
        """

        # Record the start time so that we can calculate
        # the total execution time later.
        self.start_time = time.time()
        print("before agent triggered")

    # --------------------------------------------------------
    # 2.2 BEFORE MODEL
    # --------------------------------------------------------

    def before_model(self, state: AgentState, runtime):
        """
        Called immediately before the language model is invoked.
        """

        print("before model")

    # --------------------------------------------------------
    # 2.3 AFTER MODEL
    # --------------------------------------------------------

    def after_model(self, state: AgentState, runtime):
        """
        Called immediately after the language model
        has generated a response.
        """

        print("after model")

    # --------------------------------------------------------
    # 2.4 AFTER AGENT
    # --------------------------------------------------------

    def after_agent(self, state: AgentState, runtime):
        """
        Called after the agent has completed its execution.
        """

        # Calculate the total execution time.
        elapsed_time = time.time() - self.start_time
        print(f"after agent: {elapsed_time:.2f} seconds")


# ============================================================
# 3. INITIALIZE THE CHAT MODEL
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
# 4. ALTERNATIVE MODEL CONFIGURATION
# ============================================================

# Another option is to use LangChain's init_chat_model().
#
# This example is commented out because we are currently
# using ChatOllama with a local Ollama model.
#
# model = init_chat_model(
#     model="gpt-4.1-mini",
#     temperature=0.1
# )


# ============================================================
# 5. CREATE THE AGENT
# ============================================================

# AgentMiddleware provides lifecycle hooks that allow us 
# to execute custom logic at different stages of the agent's execution.
# By attaching the custom middleware to the agent, 
# the HooksDemo middleware will automatically execute 
# its lifecycle hooks throughout the agent's lifecycle.

agent = create_agent(
    model=model,
    middleware=[HooksDemo()]
)


# ============================================================
# 6. INVOKE THE AGENT
# ============================================================

# Send a question to the agent.
response = agent.invoke(
    {
        "messages": [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="What is PCA ?")
        ]
    }
)


# ============================================================
# 7. DISPLAY RAW RESPONSE
# ============================================================

# Print the complete response returned by the agent.
# This can contain all messages exchanged during execution,
# including the final AI response.
print("\n" + 60 * "=")
print("Raw Response:")
print(response)


# ============================================================
# 8. DISPLAY CLEAN RESPONSE
# ============================================================

# Retrieve the last message from the conversation.
# This is normally the final answer generated by the model.
final_message = response["messages"][-1]

print("\nClean Response:")
print(final_message.content)