from load_chat import get_chat_model

# Initialize the model based on configuration
chat_model = get_chat_model()

# Use .invoke() as it is the current LangChain standard (replaces .predict())
response = chat_model.invoke("hi!")

# Extracting content from the message object
print(response.content)