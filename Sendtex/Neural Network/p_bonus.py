"""
Applying Categorical Cross Entropy loss to our NNFS framework
Associated with YT NNFS tutorial: https://www.youtube.com/watch?v=levekYbxauw&list=PLQVvvaa0QuDcjD5BAw2DxE6OF2tius3V3&index=8
"""

import numpy as np 
import matplotlib.pyplot as plt
from itertools import product

np.set_printoptions(precision=2, suppress=True)

np.set_printoptions(
    threshold=np.inf,       # Affiche tout
    linewidth=200,          # Largeur max avant saut de ligne
    edgeitems=10,           # Combien d’éléments afficher en début/fin si tronqué
    precision=3,            # Nombre de décimales
    suppress=True           # Ne pas utiliser la notation scientifique
)

def Label_binarizer(y):
    # Trouver les classes uniques dans y
    classes = np.unique(y)
    
    # Créer une matrice de zéros de forme (n_samples, n_classes)
    one_hot = np.zeros((y.size, classes.size))
    
    # Remplir la matrice avec des 1 aux positions appropriées
    for i, label in enumerate(y):
        one_hot[i, np.where(classes == label)[0]] = 1
    
    return np.int8(one_hot)

class Layer_Dense:

    def __init__(self, n_inputs, n_neurons):
        self.weights = np.random.randn(n_inputs, n_neurons)  * 2 - 1
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases
        
    def backward(self, learning_rate,):

        m = self.inputs.shape[0]
        gradients_weight = 1 / m * np.dot(self.inputs.T, self.dZ)               #dL/dW
        gradients_biases = np.mean(self.dZ, axis=0, keepdims=True)              #dL/db
        self.dA = np.dot(self.dZ, self.weights.T)                               #dL/dA
        
        self.weights -= learning_rate * gradients_weight
        self.biases -= learning_rate * gradients_biases


class Activation_ReLU:

    def forward(self, inputs):
        self.inputs = inputs
        self.output = np.where(self.inputs < 0, 0, self.inputs)

    def backward(self):
        self.derivative = np.where(self.inputs < 0, 0, 1)

class Activation_Softmax:

    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities  

class Loss:

    def calculate(self, output, y):
        sample_losses = self.forward(output, y)
        data_loss = np.mean(sample_losses)
        return data_loss


class Loss_CategoricalCrossentropy(Loss):

    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1-1e-7)

        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[range(samples), y_true]

        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(y_pred_clipped*y_true, axis=1)

        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods




#INITIALISATION
# Génération de toutes les combinaisons de 3 bits (0 et 1)
n = 4
combinations = list(product([0, 1], repeat=n))

# Conversion en tableau numpy
X = np.array(combinations)
y = np.arange(np.power(2, n))
y =  Label_binarizer(y)

learning_rate  = 0.001

dense1 = Layer_Dense(4,32)
activation1 = Activation_ReLU()
dense2 = Layer_Dense(32, 16)
activation2 = Activation_Softmax()

for i in range(50000):

    #Forward
    #Laywer1
    dense1.forward(X)
    activation1.forward(dense1.output)

    #Laywer2
    dense2.forward(activation1.output)
    activation2.forward(dense2.output)

    loss_function = Loss_CategoricalCrossentropy()
    loss = loss_function.calculate(activation2.output, y)

    if i % 1000 == 0:
        print("Loss:", loss)

    #Backward
    dense2.dZ = activation2.output - y              #dL/dZ2
    dense2.backward(learning_rate)                  #dL/dW2 
    activation1.backward()
    
    dense1.dZ = dense2.dA * activation1.derivative  #dL/dZ1
    dense1.backward(learning_rate)                  #dL/dZ1

y_pred = activation2.output
print(y_pred)
print(y)
print(y_pred - y)

y_pred_labels = np.argmax(y_pred, axis=1)
y_true_labels = np.argmax(y, axis=1)

accuracy = np.mean(y_pred_labels == y_true_labels)
print("Accuracy:", accuracy)