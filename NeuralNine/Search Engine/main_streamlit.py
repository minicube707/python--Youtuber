import txtai
import numpy as np
import pandas as pd
import streamlit as st


# Cache the function so the data and embeddings are loaded only once
# instead of being reloaded every time Streamlit reruns the application
@st.cache_data
def load_data_and_embedding():
    # Set a random seed to make the sampling reproducible
    np.random.seed(1)

    # Load the dataset from the CSV file
    df = pd.read_csv("train.csv")

    # Select the TITLE column and remove missing values
    # Then randomly sample 100,000 titles
    # random_state ensures that the same titles are selected each time
    titles = df["TITLE"].dropna().sample(100_000, random_state=1).values

    # Create an embeddings object using the MiniLM model
    # The model converts text into numerical vectors
    # that can be compared based on semantic similarity
    embeddings = txtai.Embeddings({
        "path": "sentence-transformers/all-MiniLM-L6-v2"
    })

    # Load the pre-built embeddings index from disk
    # This avoids having to rebuild the index every time
    # the Streamlit application starts
    embeddings.load("embeddings.tar.gz")

    # Return both the titles and the embeddings index
    return titles, embeddings


# Load the data and embeddings
titles, embeddings = load_data_and_embedding()


# Display the application title
st.title("Amazon Item Search Engine")


# Create a text input where the user can enter a search query
query = st.text_input("Enter a search query:")


# Run the search when the user clicks the Search button
if st.button("Search"):

    # Make sure the user entered a query
    if query:

        # Perform a semantic search and return the 5 most similar results
        result = embeddings.search(query, 5)

        # Retrieve the actual titles using the indexes returned by the search
        actual_results = [titles[x[0]] for x in result]

        # Display each matching title
        for res in actual_results:
            st.write(res)

    # Display a message if the search query is empty
    else:
        st.write("Please enter a query")