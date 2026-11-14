
import nltk
from nltk.stem.lancaster import LancasterStemmer

# Initialize the Lancaster Stemmer
stemmer = LancasterStemmer()

import numpy as np
import tensorflow as tf
import random
import json


# Load the intents data from the JSON file
with open('intents.json') as file:
    data = json.load(file)


# Initialize lists to store words, labels and training data
words = []
labels = []
docs_x = []
docs_y = []


# Loop through each intent in the JSON data
for intent in data['intents']:

    # Loop through each pattern associated with the current intent
    for pattern in intent['patterns']:

        # Tokenize the pattern into individual words
        wrds = nltk.word_tokenize(pattern)

        # Add the tokenized words to the vocabulary list
        words.extend(wrds)

        # Store the tokenized pattern
        docs_x.append(wrds)

        # Store the corresponding intent tag
        docs_y.append(intent["tag"])
        
    # Add the intent tag if it is not already in the labels list
    if intent['tag'] not in labels:
        labels.append(intent['tag'])


# Apply stemming and convert all words to lowercase
words = [stemmer.stem(w.lower()) for w in words]

# Remove duplicate words and sort the vocabulary alphabetically
words = sorted(list(set(words)))

# Sort the intent labels alphabetically
labels = sorted(labels)


# Initialize the training data and output lists
training = []
output = []

# Create an empty output vector with one position for each label
out_empty = [0 for _ in range(len(labels))]


# Loop through each tokenized document
for x, doc in enumerate(docs_x):

    # Initialize an empty Bag of Words vector
    bag = []

    # Apply stemming and convert document words to lowercase
    wrds = [stemmer.stem(w.lower()) for w in doc]

    # Check whether each vocabulary word exists in the current document
    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)
        
    # Create a copy of the empty output vector
    output_row = out_empty[:]

    # Set the position corresponding to the document's intent to 1
    output_row[labels.index(docs_y[x])] = 1

    # Add the Bag of Words vector to the training data
    training.append(bag)

    # Add the corresponding one-hot encoded label to the output data
    output.append(output_row)


# Convert the training data into a NumPy array
training = np.array(training)

# Convert the output labels into a NumPy array
output = np.array(output)

print("\nVariable:")
print(f"{training=}")
print(f"{output=}")