import txtai
import pandas as pd
import streamlit as st


# Cache the function so the data and embeddings are loaded only once
# instead of being reloaded every time Streamlit reruns the application
@st.cache_data
def load_data_and_embedding():

    # Load the dataset from the CSV file
    # dropna() removes rows containing missing values
    df = pd.read_csv("seth-data.csv").dropna()

    # Extract the blog post titles and URLs
    # These arrays will be used to display the search results
    titles = df.title.values
    urls = df.url.values

    # Create an embeddings object using the MiniLM model
    # The model converts text into numerical vectors
    # that represent the semantic meaning of the content
    embeddings = txtai.Embeddings({
        "path": "sentence-transformers/all-MiniLM-L6-v2"
    })

    # Load the pre-built embeddings index from disk
    # This avoids rebuilding the index every time the application starts
    embeddings.load("embeddings_seth.tar.gz")

    # Return the titles, URLs, and embeddings index
    return titles, urls, embeddings


# Load the blog post data and embeddings
titles, urls, embeddings = load_data_and_embedding()


# Display the application title
st.title("Seth Blog Post Search Engine")


# Create a text input where the user can enter a search query
query = st.text_input("Enter a search query:")


# Run the search when the user clicks the Search button
if st.button("Search"):

    # Make sure the user entered a search query
    if query:

        # Perform a semantic search and return the 5 most similar results
        result = embeddings.search(query, 5)

        # Retrieve the title and URL for each matching result
        actual_results = [
            f"Title: {titles[x[0]]}, URL: {urls[x[0]]}"
            for x in result
        ]

        # Display each search result
        for res in actual_results:
            st.write(res)

    # Display a message if the search query is empty
    else:
        st.write("Please enter a query")