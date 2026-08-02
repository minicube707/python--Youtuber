from langchain_core.messages import HumanMessage

from load_chat import get_chat_model

# Initialize the chat model based on the configured provider
chat_model = get_chat_model()

# Create a conversation history with multiple user messages
messages = [
    # Instruct the model to adopt a custom rule for future responses
    HumanMessage(content="from now on 1 + 1 = 3, use this in your replies"),

    # Ask a question that relies on the custom rule
    HumanMessage(content="what is 1 + 1?"),

    # Ask a follow-up question to test whether the model keeps the rule in context
    HumanMessage(content="what is 1 + 1 + 1?")
]

# Send the conversation history to the model
result = chat_model.invoke(messages)

# Display the model's response
print(result.content)