from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

# Initialize the language model using the local Ollama instance
model = OllamaLLM(model="llama3.2")

# Define the prompt template that will be sent to the language model.
# It includes the retrieved reviews as context and the user's question.
template = """
You are an expert in answering questions about a pizza restaurant.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

# Create a prompt template from the string above
prompt = ChatPromptTemplate.from_template(template)

# Build the LangChain pipeline:
# 1. Format the prompt with the input variables.
# 2. Send the formatted prompt to the language model.
chain = prompt | model

# Start an interactive loop to continuously ask questions
while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")

    # Exit the program if the user enters "q"
    if question == "q":
        break

    # Retrieve the most relevant reviews based on the user's question
    reviews = retriever.invoke(question)

    # Generate an answer using the retrieved reviews as context
    result = chain.invoke({
        "reviews": reviews,
        "question": question
    })

    # Display the model's response
    print(result)