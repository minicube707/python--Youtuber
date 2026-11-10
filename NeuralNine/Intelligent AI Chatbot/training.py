
import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

# Download WordNet and initialize the lemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

# Load the chatbot intents from the JSON file
intents = json.loads(open('intents.json').read())


words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']


# Extract words, patterns and intent tags from the JSON data
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


# Clean the vocabulary by removing punctuation, applying lemmatization
# and keeping only unique words
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

print(f"\n{documents=}")
print(f"\n{words=}")

classes = sorted(set(classes))

# Save the vocabulary and intent classes for later use by the chatbot
pickle.dump(words, open('word.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))


# =====================================================
# Machine Learning Part
# =====================================================

training = []
ouput_empty = [0] * len(classes)

# Convert each training pattern into a Bag of Words representation
# Each word is represented by 1 if present, or 0 if absent
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    # Create an output vector with 1 for the corresponding intent
    # and 0 for all the other intents
    ouput_row = list(ouput_empty)
    ouput_row[classes.index(document[1])] = 1
    training.append([bag, ouput_row])

# Shuffle the training data to prevent the model from learning patterns
# based on the original order of the examples
random.shuffle(training)

# Split the data into input features (train_x) and expected outputs (train_y)
train_x = np.array([item[0] for item in training])
train_y = np.array([item[1] for item in training])


# =====================================================
# Neural Network Model
# =====================================================

# Build a neural network with two hidden layers and Dropout
# to help reduce overfitting
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]), ), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))

# The output layer uses softmax to predict the most likely intent
model.add(Dense(len(train_y[0]), activation='softmax'))

# Configure the Stochastic Gradient Descent optimizer
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model using the prepared dataset
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save the trained model for future use by the chatbot
model.save('chatbot_model.keras', hist)

print("Done")
