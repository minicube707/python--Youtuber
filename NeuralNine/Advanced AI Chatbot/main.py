
import os
import json
import random

import nltk
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


# Define the neural network architecture used by the chatbot
class ChatbotModel(nn.Module):

    def __init__(self, input_size, output_size):
        super(ChatbotModel, self).__init__()

        # First fully connected layer: transforms the input into 128 neurons
        self.fc1 = nn.Linear(input_size, 128)

        # Second fully connected layer: reduces the representation to 64 neurons
        self.fc2 = nn.Linear(128, 64)

        # Output layer: produces one score for each possible intent
        self.fc3 = nn.Linear(64, output_size)

        # ReLU activation function introduces non-linearity into the network
        self.relu = nn.ReLU()

        # Dropout randomly disables 50% of neurons during training
        # This helps prevent overfitting
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # Pass the input through the first layer and apply ReLU activation
        x = self.relu(self.fc1(x))

        # Apply dropout to reduce overfitting
        x = self.dropout(x)

        # Pass the result through the second layer and apply ReLU
        x = self.relu(self.fc2(x))

        # Apply dropout again
        x = self.dropout(x)

        # Generate the final output scores for each intent
        x = self.fc3(x)

        return x


# Main class responsible for managing the chatbot
class ChatBotAssistant():

    def __init__(self, intent_path, function_mappings=None):

        # Initialize the neural network (will be created later)
        self.model = None

        # Store the path to the JSON file containing the chatbot intents
        self.intents_path = intent_path

        # Store all tokenized training sentences and their corresponding intents
        self.documents = []

        # Store all unique words found in the training patterns
        self.vocabulary = []

        # Store the list of available intent labels
        self.intents = []

        # Dictionary mapping each intent to its possible responses
        self.intents_responses = {}

        # Store optional functions associated with specific intents
        self.function_mappings = function_mappings

        # Training data (input features and expected outputs)
        self.X = None
        self.y = None

    @staticmethod
    def tokenize_and_lemmatize(text):
        # Initialize the WordNet lemmatizer to reduce words to their base form
        lemmatizer = nltk.WordNetLemmatizer()

        # Split the input sentence into individual words
        words = nltk.word_tokenize(text)

        # Convert words to lowercase and apply lemmatization
        words = [lemmatizer.lemmatize(word.lower()) for word in words]

        return words

    def bag_of_words(self, words):
        # Convert a sentence into a binary vector based on the vocabulary
        # A value of 1 means the word is present, while 0 means it is absent
        return [1 if word in words else 0 for word in self.vocabulary]

    def parse_intents(self):

        # Check whether the JSON intents file exists
        if os.path.exists(self.intents_path):

            # Open and load the JSON file
            with open(self.intents_path, 'r') as f:
                intents_data = json.load(f)

            # Iterate through all intents defined in the JSON file
            for intent in intents_data['intents']:

                # Add the intent if it has not already been registered
                if intent['tag'] not in self.intents:
                    self.intents.append(intent['tag'])

                    # Store all possible responses associated with this intent
                    self.intents_responses[intent['tag']] = intent['responses']

                # Process each example sentence associated with the intent
                for pattern in intent['patterns']:

                    # Tokenize and lemmatize the example sentence
                    pattern_words = self.tokenize_and_lemmatize(pattern)

                    # Add the words to the vocabulary
                    self.vocabulary.extend(pattern_words)

                    # Store the processed sentence together with its intent
                    self.documents.append((pattern_words, intent['tag']))

            # Remove duplicate words and sort the vocabulary alphabetically
            self.vocabulary = sorted(set(self.vocabulary))

    def prepare_data(self):
        # Lists used to store the input vectors and their corresponding labels
        bags = []
        indices = []

        # Process every training document
        for document in self.documents:

            # Extract the tokenized words from the current document
            words = document[0]

            # Convert the words into a Bag of Words vector
            bag = self.bag_of_words(words)

            # Convert the intent label into its numerical index
            intent_index = self.intents.index(document[1])

            # Add the input vector and its corresponding intent index
            bags.append(bag)
            indices.append(intent_index)

        # Convert the training data into NumPy arrays
        self.X = np.array(bags)
        self.y = np.array(indices)

    def train_model(self, batch_size, lr, epochs):

        # Convert the NumPy arrays into PyTorch tensors
        # Inputs use float32, while labels use long integers
        X_tensor = torch.tensor(self.X, dtype=torch.float32)
        y_tensor = torch.tensor(self.y, dtype=torch.long)

        # Combine input features and labels into a dataset
        dataset = TensorDataset(X_tensor, y_tensor)

        # Create a DataLoader to divide the dataset into batches
        # Shuffle the data at each epoch to improve training
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        # Initialize the neural network using the input and output dimensions
        self.model = ChatbotModel(self.X.shape[1], len(self.intents))

        # CrossEntropyLoss measures the difference between predictions and true labels
        criterion = nn.CrossEntropyLoss()

        # Adam optimizer updates the network weights during training
        optimizer = optim.Adam(self.model.parameters(), lr=lr)

        # Training loop: repeat the process for the specified number of epochs
        for epoch in range(epochs):

            # Initialize metrics for the current epoch
            running_loss = 0.0
            correct = 0
            total = 0

            # Iterate through each batch of training data
            for batch_X, batch_y in loader:

                # Reset gradients from the previous iteration
                optimizer.zero_grad()

                # Forward pass: generate predictions using the neural network
                outputs = self.model(batch_X)

                # Calculate the loss between predictions and expected labels
                loss = criterion(outputs, batch_y)

                # Backward pass: calculate gradients
                loss.backward()

                # Update the model parameters using the optimizer
                optimizer.step()

                # Accumulate the loss for the current epoch
                running_loss += loss.item()

                # Calculate the predicted intent for each sample in the batch
                predictions = torch.argmax(outputs, dim=1)

                # Count the number of correct predictions
                correct += (predictions == batch_y).sum().item()

                # Count the total number of processed samples
                total += batch_y.size(0)

            # Calculate the average loss for the current epoch
            epoch_loss = running_loss / len(loader)

            # Calculate the classification accuracy as a percentage
            accuracy = 100 * correct / total

            # Display the training results for the current epoch
            print(f"Epoch {epoch+1}/{epochs} - Loss: {epoch_loss:.4f} - Accuracy: {accuracy:.2f}%")

    def save_model(self, model_path, dimension_path):

        # Save the trained neural network weights
        torch.save(self.model.state_dict(), model_path)

        # Save the input and output dimensions needed to recreate the model
        with open(dimension_path, 'w') as f:
            json.dump({'input_size': self.X.shape[1], 'output_size': len(self.intents)}, f)

    def load_model(self, model_path, dimensions_path):

        # Load the model dimensions from the JSON file
        with open(dimensions_path, 'r') as f:
            dimensions = json.load(f)

        # Recreate the neural network using the saved dimensions
        self.model = ChatbotModel(
            dimensions['input_size'],
            dimensions['output_size']
        )

        # Load the previously trained weights into the neural network
        self.model.load_state_dict(torch.load(model_path, weights_only=True))

    def process_message(self, input_message):

        # Tokenize and lemmatize the user's input message
        words = self.tokenize_and_lemmatize(input_message)

        # Convert the message into a Bag of Words vector
        bag = self.bag_of_words(words)

        # Convert the vector into a PyTorch tensor
        # The extra dimension represents the batch size (1 message)
        bag_tensor = torch.tensor([bag], dtype=torch.float32)

        # Switch the model to evaluation mode (disables dropout)
        self.model.eval()

        # Disable gradient calculations since the model is only making predictions
        with torch.no_grad():

            # Pass the input message through the neural network
            prediction = self.model(bag_tensor)

        # Find the index of the intent with the highest prediction score
        predicted_class_index = torch.argmax(prediction, dim=1).item()

        # Convert the predicted index back into its corresponding intent label
        predicted_intent = self.intents[predicted_class_index]

        # Check whether a custom function is associated with the predicted intent
        if self.function_mappings:

            if predicted_intent in self.function_mappings:

                # Execute the function associated with the detected intent
                self.function_mappings[predicted_intent]()

        # Check whether the predicted intent has predefined responses
        if self.intents_responses[predicted_intent]:

            # Randomly select one response from the available responses
            return random.choice(self.intents_responses[predicted_intent])

        else:
            # Return None if no response is available for this intent
            return None


# Example function that displays three randomly selected stock symbols
def get_stocks():

    # List of stock market symbols
    stocks = ['AAPL', 'META', 'NVDA', 'GS', 'MSFT']

    # Randomly select and print three stocks without repetition
    print(random.sample(stocks, 3))


# Entry point of the program
# This block only executes when the Python file is run directly
if __name__ == "__main__":

    # Example training workflow (currently commented out)
    # assistant = ChatBotAssistant('intents.json', function_mappings={'stocks': get_stocks})
    # assistant.parse_intents()
    # assistant.prepare_data()
    # assistant.train_model(batch_size=8, lr=0.001, epochs=100)

    # Save the trained model and its dimensions
    # assistant.save_model('chatbot_model.pth', 'dimensions.json')

    # Create a chatbot instance and associate the 'stocks' intent with get_stocks()
    assistant = ChatBotAssistant(
        'intents.json',
        function_mappings={'stocks': get_stocks}
    )

    # Load the intents and build the vocabulary
    assistant.parse_intents()

    # Load the previously trained neural network
    assistant.load_model('chatbot_model.pth', 'dimensions.json')

    # Start an infinite loop to interact with the chatbot
    while True:

        # Ask the user to enter a message
        message = input('Enter your message: ')

        # Exit the chatbot when the user types '/quit'
        if message == '/quit':
            break

        # Process the message and display the chatbot's response
        print("bot: ", assistant.process_message(message))
