
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


# Initialize lists to store words, labels and training documents
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

        # Add the tokenized words to the vocabulary
        words.extend(wrds)

        # Store the tokenized pattern
        docs_x.append(wrds)

        # Store the corresponding intent tag
        docs_y.append(intent["tag"])
        
    # Add the intent tag if it is not already in the labels list
    if intent['tag'] not in labels:
        labels.append(intent['tag'])


# Apply stemming, convert words to lowercase and exclude question marks
words = [stemmer.stem(w.lower()) for w in words if w not in "?"]

# Remove duplicate words and sort the vocabulary alphabetically
words = sorted(list(set(words)))

# Sort the intent labels alphabetically
labels = sorted(labels)


# Initialize the training data and output lists
training = []
output = []

# Create an empty output vector with one position for each intent label
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

    # Set the corresponding intent position to 1 (One-Hot Encoding)
    output_row[labels.index(docs_y[x])] = 1

    # Add the Bag of Words vector to the training data
    training.append(bag)

    # Add the corresponding output vector
    output.append(output_row)


# Convert the training data into a NumPy array
training = np.array(training)

# Convert the output data into a NumPy array
output = np.array(output)


# Define the neural network architecture
model = tf.keras.Sequential([

    # Define the input layer with the vocabulary size
    tf.keras.layers.Input(shape=(len(training[0]),)),

    # First hidden layer with 8 neurons and linear activation
    tf.keras.layers.Dense(8, activation="linear"),

    # Second hidden layer with 8 neurons and linear activation
    tf.keras.layers.Dense(8, activation="linear"),

    # Output layer with one neuron per intent and softmax activation
    tf.keras.layers.Dense(len(output[0]), activation="softmax")
])


# Configure the model for training
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


# Train the neural network using the training data
model.fit(
    training,
    output,
    epochs=1000,
    batch_size=8,
    verbose=1
)


# Save the trained model to a Keras file
model.save("model.keras")
