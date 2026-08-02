from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import BaseOutputParser

from load_chat import get_chat_model

# Initialize the chat model based on the configured provider
chat_model = get_chat_model()


class AnswerOutputParser(BaseOutputParser):
    """
    Custom output parser that extracts the reasoning steps
    and the final answer from the model response.
    """

    def parse(self, text: str):
        """
        Parse the output of an LLM response.

        The model is expected to return the final answer
        using the format: "answer = <answer here>"
        """
        # Split the response into the explanation steps and the final answer
        return text.strip().split("answer =")


# Define the system prompt that explains the assistant's task
template = """
You are a helpful assistant that solves math problems and shows your work.
Output each step then return the answer in the following format:
answer = <answer here>.

Make sure to output answer in all lowercase and to have exactly one space
and one equal sign following it.
"""

# Define the template for the user's math problem
human_template = "{problem}"

# Create a chat prompt containing system instructions and user input
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

# Format the prompt with a specific math problem
messages = chat_prompt.format_messages(
    problem="2x^2 - 5x + 3 = 0"
)

# Send the formatted messages to the language model
result = chat_model.invoke(messages)

# Parse the model response to separate the steps and the final answer
parsed = AnswerOutputParser().parse(result.content)
steps, answer = parsed

# Display the reasoning steps and the extracted answer
print(steps, answer)