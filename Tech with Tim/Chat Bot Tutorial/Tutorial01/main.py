
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

print("\nJSON file:\n", json.dumps(data, indent=4))


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
        
    # Add the intent tag to the labels list if it is not already present
    if intent['tag'] not in labels:
        labels.append(intent['tag'])


# Display the extracted words, labels and training documents
print("\nVariable:")
print(f'\n{words=}')
print(f'\n{labels=}')
print(f'\n{docs_x=}')
print(f'\n{docs_y=}')
