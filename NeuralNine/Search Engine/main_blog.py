import txtai
import pandas as pd

# Load the dataset from the CSV file
# dropna() removes rows containing missing values
df = pd.read_csv("seth-data.csv").dropna()

# Extract the content_plain column as a NumPy array
# These texts will be converted into embeddings
content = df.content_plain.values

# Create an embeddings object using the MiniLM model
# The model converts each text into a numerical vector
# that captures its semantic meaning
embeddings = txtai.Embeddings({
    "path": "sentence-transformers/all-MiniLM-L6-v2"
})

# Convert all text content into embeddings
# and build the search index
# This allows us to perform semantic searches later
embeddings.index(content)

# Save the embeddings index to a file
# The index can be loaded later without rebuilding it
embeddings.save("embeddings_seth.tar.gz")