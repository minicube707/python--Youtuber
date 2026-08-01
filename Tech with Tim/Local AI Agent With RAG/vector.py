from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load the restaurant reviews dataset from a CSV file
df = pd.read_csv("realistic_restaurant_reviews.csv")

# Initialize the embedding model used to convert text into vector representations
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Define the location where the Chroma vector database will be stored
db_location = "./chrome_langchain_db"

# Only create and populate the database if it does not already exist
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    # Convert each review into a LangChain Document
    for i, row in df.iterrows():
        document = Document(
            
            # Combine the review title and content into a single searchable text
            page_content=row["Title"] + " " + row["Review"],

            # Store additional information as metadata
            metadata={
                "rating": row["Rating"],
                "date": row["Date"]
            },

            # Assign a unique ID to each document
            id=str(i)
        )

        ids.append(str(i))
        documents.append(document)

# Create or load the Chroma vector store
vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

# Add all documents to the vector database only during the initial setup
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# Create a retriever that returns the 5 most relevant documents for a query
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)