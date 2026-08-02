from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import BaseOutputParser

from load_chat import get_chat_model

# Initialize the chat model based on the configured provider
chat_model = get_chat_model()


class CommaSeparatedListOutputParser(BaseOutputParser):
    """
    Custom output parser that converts a comma-separated string
    returned by the model into a Python list.
    """

    def parse(self, text: str):
        """
        Parse the model output by splitting values separated by commas.

        Example:
        "red, blue, green" -> ["red", "blue", "green"]
        """
        return text.strip().split(", ")


# Define the system prompt that specifies the model's expected behavior
template = """
You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category
in a comma separated list.

ONLY return a comma separated list, and nothing more.
"""

# Define the template for the user's category input
human_template = "{text}"

# Create a prompt template with system instructions and user input
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

# Build a processing chain:
# 1. Format the prompt
# 2. Send it to the language model
# 3. Parse the output into a Python list
chain = chat_prompt | chat_model | CommaSeparatedListOutputParser()

# Invoke the chain with a category and get the parsed result
result = chain.invoke({"text": "colors"})

# Display the generated list
print(result)