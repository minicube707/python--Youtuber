"""
Applying Categorical Cross Entropy loss to our NNFS framework
Associated with YT NNFS tutorial: https://www.youtube.com/watch?v=levekYbxauw&list=PLQVvvaa0QuDcjD5BAw2DxE6OF2tius3V3&index=8
"""

import numpy as np 
import matplotlib.pyplot as plt

def spiral_data(samples, classes):
    X = np.zeros((samples*classes, 2))
    y = np.zeros(samples*classes, dtype='uint8')
    for class_number in range(classes):
        ix = range(samples*class_number, samples*(class_number+1))
        r = np.linspace(0.0, 1, samples)  # radius
        t = np.linspace(class_number*4, (class_number+1)*4, samples) + np.random.randn(samples)*0.2
        X[ix] = np.c_[r*np.sin(t*2.5), r*np.cos(t*2.5)]
        y[ix] = class_number
    return X, y


def Label_binarizer(y):
    # Trouver les classes uniques dans y
    classes = np.unique(y)
    
    # Créer une matrice de zéros de forme (n_samples, n_classes)
    one_hot = np.zeros((y.size, classes.size))
    
    # Remplir la matrice avec des 1 aux positions appropriées
    for i, label in enumerate(y):
        one_hot[i, np.where(classes == label)[0]] = 1
    
    return np.int8(one_hot)

def graph(X, y):
    plt.figure(figsize=(6, 6))
    plt.scatter(X[:, 0], X[:, 1], c=y)
    plt.title("Spiral Dataset")
    plt.xlabel("X1")
    plt.ylabel("X2")
    plt.axis('equal')

    plt.figure(figsize=(6, 6))
    plt.scatter(X[:, 0], X[:, 1])
    plt.title("Spiral Dataset")
    plt.xlabel("X1")
    plt.ylabel("X2")
    plt.axis('equal')
    plt.show()

class Layer_Dense:

    def __init__(self, n_inputs, n_neurons):
        self.weights = np.random.randn(n_inputs, n_neurons)  * 2 - 1
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases
        
    def backward(self, learning_rate):

        m = self.inputs.shape[0]
        gradients_weight = 1 / m * np.dot(self.inputs.T, self.dZ)               #dL/dW2 
        gradients_biases = np.mean(self.dZ, axis=0, keepdims=True)              #dL/db2
        self.dA = np.dot(self.dZ, self.weights.T)                               #dL/dA
        
        self.weights -= learning_rate * gradients_weight
        self.biases -= learning_rate * gradients_biases


class Activation_ReLU:

    def forward(self, inputs):
        self.inputs = inputs
        self.output = np.where(self.inputs < 0, 0, self.inputs)

    def backward(self):
        self.derivative = np.where(self.inputs < 0, 0, 1)

class Activation_Sigmoide:

    def forward(self, inputs):
        self.output = 1/(1 + np.exp(-inputs))

    def backward(self):
        self.derivative = self.output * (1 - self.output)

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




X, y = spiral_data(samples=100, classes=3)
graph(X, y)

new_X = np.column_stack((
    np.sqrt(X[:,0]**2 + X[:,1]**2),  # rayon
    np.arctan2(X[:,1], X[:,0])  # angle
))

y =  Label_binarizer(y)

learning_rate  = 0.001

dense1 = Layer_Dense(2,64)
activation1 = Activation_Sigmoide()

dense2 = Layer_Dense(64, 128)
activation2 = Activation_Sigmoide()

dense3 = Layer_Dense(128, 32)
activation3 = Activation_ReLU()

dense4 = Layer_Dense(32, 3)
activation4 = Activation_Softmax()

for i in range(50000):

    #Forward
    #Layer1
    dense1.forward(new_X)
    activation1.forward(dense1.output)

    #Layer2
    dense2.forward(activation1.output)
    activation2.forward(dense2.output)

    #Layer3
    dense3.forward(activation2.output)
    activation3.forward(dense3.output)

    #Layer4
    dense4.forward(activation3.output)
    activation4.forward(dense4.output)

    loss_function = Loss_CategoricalCrossentropy()
    loss = loss_function.calculate(activation4.output, y)

    if i % 1000 == 0:
        print("Loss:", loss)

    #Backward
    dense4.dZ = activation4.output - y              #dL/dZ4
    dense4.backward(learning_rate)                  #dL/dW4 
    activation3.backward()
    
    dense3.dZ = dense4.dA * activation3.derivative  #dL/dZ3
    dense3.backward(learning_rate)                  #dL/dZ3
    activation2.backward()

    dense2.dZ = dense3.dA * activation2.derivative  #dL/dZ2
    dense2.backward(learning_rate)                  #dL/dZ2
    activation1.backward()

    dense1.dZ = dense2.dA * activation1.derivative  #dL/dZ1
    dense1.backward(learning_rate)                  #dL/dZ1

y_pred = activation4.output
y_pred_labels = np.argmax(y_pred, axis=1)
graph(X, y_pred_labels)