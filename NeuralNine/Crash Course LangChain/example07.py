from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.tools import create_retriever_tool
from langchain.agents import create_agent
# from langchain_openai import OpenAIEmbeddings


# ============================================================
# 1. MODEL CONFIGURATION
# ============================================================

# Name of the Ollama chat model used by the agent.
MODEL = "qwen3.5:9b"

# Name of the Ollama embedding model used to convert text
# into numerical vectors.
MODEL_EMBEDDING = "mxbai-embed-large:latest"


# ============================================================
# 2. EMBEDDING MODEL
# ============================================================

# Initialize the Ollama embedding model.
# This model converts text into vectors that can be compared
# using semantic similarity.
embeddings = OllamaEmbeddings(
    model=MODEL_EMBEDDING
)

# Example: OpenAI embeddings could be used instead.
# from langchain_openai import OpenAIEmbeddings
#
# embeddings = OpenAIEmbeddings(
#     model="text-embedding-3-large"
# )


# ============================================================
# 3. FIRST KNOWLEDGE BASE
# ============================================================

# Small dataset containing information about computers,
# fruits, and personal preferences.
texts1 = [
    "Apple makes very good computers.",
    "I believe Apple is innovative!",
    "I love apples",
    "I am a fan of MacBooks.",
    "I enjoy oranges.",
    "I like Lenovo ThinkPads.",
    "I think pears taste very good."
]


# ============================================================
# 4. CREATE THE FIRST FAISS VECTOR STORE
# ============================================================

# Create a FAISS vector database from the text documents.
# Each text is converted into an embedding before being stored.
vector_store = FAISS.from_texts(
    texts1,
    embedding=embeddings
)


# ============================================================
# 5. SIMILARITY SEARCH
# ============================================================

# Display a separator to make the console output easier to read.
print(60 * "=")
print("Similarity Search Results:")


# ------------------------------------------------------------
# 5.1 Apple-related query
# ------------------------------------------------------------

print("\n--- Apple Query ---")

# Search for the 7 documents that are semantically closest
# to the query.
results = vector_store.similarity_search("Apple is my favorite food.", k=7)

# Display the content of each retrieved document.
for doc in results:
    print(doc.page_content)


# ------------------------------------------------------------
# 5.2 Linux-related query
# ------------------------------------------------------------

print("\n--- Linux Query ---")

# Search for documents that are semantically similar
# to a Linux-related question.
results = vector_store.similarity_search("Linux is a great operating system.", k=7)

# Display the retrieved documents.
for doc in results:
    print(doc.page_content)


# ============================================================
# 6. SECOND KNOWLEDGE BASE
# ============================================================

# This dataset contains information about fruits and
# operating system preferences.
texts2 = [
    "I love apples",
    "I enjoy oranges.",
    "I think pears taste very good.",
    "I hate bananas",
    "I dislike raspberries",
    "I despise mangos",
    "I love Linux",
    "I hate Windows"
]


# ============================================================
# 7. CREATE THE SECOND FAISS VECTOR STORE
# ============================================================

# Replace the previous vector store with a new one
# containing the second dataset.
vector_store = FAISS.from_texts(
    texts2,
    embedding=embeddings
)


# ============================================================
# 8. DIRECT SIMILARITY SEARCH
# ============================================================

# Search for the three documents most similar to the question
# about fruits that the person likes.
print("\n--- Fruits the person likes ---")

results = vector_store.similarity_search("What fruits does the person like?", k=3)

for doc in results:
    print(doc.page_content)


# Search for the three documents most similar to the question
# about fruits that the person dislikes.
print("\n--- Fruits the person dislikes ---")

results = vector_store.similarity_search("What fruits does the person hate?", k=3)

for doc in results:
    print(doc.page_content)


# ============================================================
# 9. CREATE A RETRIEVER
# ============================================================

# Convert the FAISS vector store into a retriever.
# The retriever will return the 3 most relevant documents
# for each query.
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# ============================================================
# 10. CREATE THE RETRIEVER TOOL
# ============================================================

# Convert the retriever into a tool that can be called
# by the LangChain agent.
retriever_tool = create_retriever_tool(
    retriever,
    name="kb_search",
    description=(
        "Search the small product, fruit, and preference "
        "knowledge base for relevant information."
    )
)


# ============================================================
# 11. INITIALIZE THE CHAT MODEL
# ============================================================

# Initialize the Ollama chat model.
# Temperature 0 makes the model's responses more deterministic.
model = ChatOllama(
    model=MODEL,
    temperature=0
)


# ============================================================
# 12. CREATE THE AGENT
# ============================================================

# Create an agent that has access to the knowledge base
# through the kb_search tool.
agent = create_agent(
    model=model,
    tools=[retriever_tool],
    system_prompt=(
        "You are a helpful assistant. "
        "For questions about Macs, Apple, fruits, or laptops, "
        "first call the kb_search tool to retrieve relevant context. "
        "You may call the tool multiple times if necessary before "
        "providing the final answer. "
        "Answer succinctly."
    )
)


# ============================================================
# 13. SEND A QUESTION TO THE AGENT
# ============================================================

# Send a user question to the agent.
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "What three fruits does the person like "
                    "and what three fruits does the person dislike?"
                )
            }
        ]
    }
)


# ============================================================
# 14. DISPLAY RAW RESPONSE
# ============================================================

# Print the complete response returned by the agent.
# This can contain all the messages exchanged during execution,
# including tool calls and the final answer.
print("\n" + 60 * "=")
print("Raw Response:")
print(response)


# ============================================================
# 15. DISPLAY CLEAN RESPONSE
# ============================================================

# Print only the content of the agent's final message.
# The last message usually contains the final answer intended
# for the user.
print("\nClean Response:")
print(response["messages"][-1].content)