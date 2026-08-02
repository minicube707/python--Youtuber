from langchain_core.prompts import ChatPromptTemplate

from load_chat import get_chat_model

# Initialize the chat model based on the configured provider
chat_model = get_chat_model()

# Define the system prompt that describes the assistant's role
system_template = (
    "You are a helpful assistant that translates {input_language} "
    "to {output_language}."
)

# Define the template for the user's input
human_template = "{text}"

# Create a chat prompt template with system and human messages
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_template),
])

# Populate the prompt template with the desired languages and text
messages = chat_prompt.format_messages(
    input_language="English",
    output_language="French",
    text="I love programming."
)

# Send the formatted messages to the model
result = chat_model.invoke(messages)

# Display the translated text
print(result.content)