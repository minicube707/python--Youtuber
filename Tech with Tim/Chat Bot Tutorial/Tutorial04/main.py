
import nltk
from nltk.stem.lancaster import LancasterStemmer

# Initialize the Lancaster Stemmer
stemmer = LancasterStemmer()

import numpy as np
import tensorflow as tf
import random
import json
import pickle


# Load the intents data from the JSON file
with open('intents.json') as file:
    data = json.load(file)


# Try to load the preprocessed training data from the pickle file
try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

# If the pickle file does not exist, preprocess the data
except:
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


    # Convert the training data into NumPy arrays
    training = np.array(training)
    output = np.array(output)

    # Save the preprocessed data to a pickle file for future use
    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)


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


# Try to load an already trained model
try:
    model = tf.keras.models.load_model("model.keras")

# If the model does not exist, train and save a new one
except:
    # Train the neural network using the training data
    model.fit(training, output, epochs=1000, batch_size=8, verbose=1)

    # Save the trained model
    model.save("model.keras")


# Convert a sentence into a Bag of Words representation
def bag_of_words(s, words):

    # Initialize a vector filled with zeros
    bag = [0 for _ in range(len(words))]

    # Tokenize the input sentence
    s_words = nltk.word_tokenize(s)

    # Apply stemming and convert all words to lowercase
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    # Compare each input word with the vocabulary
    for se in s_words:
        for i, w in enumerate(words):

            # Set the corresponding position to 1 if the word is found
            if w == se:
                bag[i] = 1

    # Return the Bag of Words vector as a NumPy array
    return np.array(bag)


# Define the chatbot interaction function
def chat():
    
    # Display the chatbot startup message
    print("\nStart talking with the bot (type quit to stop)!")

    # Keep the conversation running until the user types "quit"
    while True:

        # Get the user's input
        inp = input("You: ")

        # Stop the conversation if the user types "quit"
        if inp.lower() == "quit":
            break
        
        # Convert the user's input into a Bag of Words vector
        bow = bag_of_words(inp, words)

        # Predict the intent probabilities using the trained model
        results = model.predict(np.array([bow]), verbose=0)[0]

        # Get the index of the intent with the highest probability
        results_index = np.argmax(results)

        # Retrieve the predicted intent tag
        tag = labels[results_index]

        # Find the corresponding intent in the JSON data
        for tg in data["intents"]:
            if tg['tag'] == tag:

                # Retrieve the possible responses for this intent
                responses = tg['responses']

        # Select and display a random response
        print("bot: ", random.choice(responses))


# Start the chatbot
chat()
