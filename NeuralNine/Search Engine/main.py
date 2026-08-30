import txtai
import numpy as np
import pandas as pd

# Set a random seed to make the sampling reproducible
np.random.seed(1)

# Load the training dataset from the CSV file
df = pd.read_csv("train.csv")

# Select the TITLE column, remove missing values,
# and randomly sample 100,000 titles
# random_state ensures that we always get the same samples
titles = df["TITLE"].dropna().sample(100_000, random_state=1).values

# Create an embeddings object using the MiniLM model
# This model converts text into numerical vectors
# that can be compared to measure semantic similarity
embeddings = txtai.Embeddings({
    "path": "sentence-transformers/all-MiniLM-L6-v2"
})

# Convert all titles into embeddings and build the search index
# This allows us to perform fast semantic searches later
embeddings.index(titles)

# Save the embeddings index to a file
# This means we don't need to rebuild the index every time
# we run the application
embeddings.save("embeddings.tar.gz")

# Perform a semantic search using the query
# The search returns the 5 most similar titles
result = embeddings.search("protector for cam", limit=5)

# Display the search results
# Each result contains the index of the title and its similarity score
print(result)

# Retrieve the actual titles using the indexes returned by the search
actual_results = [titles[x[0]] for x in result]

# Display the matching titles
print(actual_results)