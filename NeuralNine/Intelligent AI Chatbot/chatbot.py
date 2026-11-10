
import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model


# Download WordNet and initialize the lemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

# Load the intents, vocabulary, classes and trained chatbot model
intents = json.loads(open('intents.json').read())

words = pickle.load(open('word.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.keras')


# Tokenize the input sentence and reduce words to their base form
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


# Convert the input sentence into a Bag of Words vector
# Each position represents a word from the vocabulary:
# 1 if the word is present, 0 otherwise
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    
    return np.array(bag)


# Predict the intent of the user's message using the trained model
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]

    # Keep only predictions with a probability above the threshold
    ERROR_THRESHOLD = 0.25
    result = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # Sort predictions by probability, from highest to lowest
    result.sort(key=lambda x: x[1], reverse=True)

    # Convert predictions into a list containing intent names and probabilities
    return_list = []
    for r in result:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


# Find the response associated with the predicted intent
# and randomly select one of the available responses
def get_response(intent_list, intent_json):
    tag = intent_list[0]['intent']
    list_of_intents = intent_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


# Start the chatbot conversation loop
print("")
print("Go! Bot is running!")

while True:
    message = input("You: ")
    ints = predict_class(message)
    res = get_response(ints, intents)
    print("Bot: ", res)
