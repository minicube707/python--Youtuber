"""
Applying Categorical Cross Entropy loss to our NNFS framework
Associated with YT NNFS tutorial: https://www.youtube.com/watch?v=levekYbxauw&list=PLQVvvaa0QuDcjD5BAw2DxE6OF2tius3V3&index=8
"""

import numpy as np 

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


class Layer_Dense:

    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

    def backward(self, dZ, learning_rate):
        m = self.output.shape[1]  

        gradients_weight = 1 / m * np.dot(self.output.T, dZ)
        gradients_biases = 1 / m * np.mean(dZ, axis=0, keepdims=True)    
        self.dA = np.dot(dZ, self.weights.T)

        self.weights -= learning_rate * gradients_weight
        self.biases -= learning_rate * gradients_biases


class Activation_ReLU:

    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

    def backward(self):
        self.derivative = np.where(X < 0, 0, X)
    
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
y =  Label_binarizer(y)

learning_rate  = 0.01

dense1 = Layer_Dense(2,5)
activation1 = Activation_ReLU()
dense2 = Layer_Dense(5, 3)
activation2 = Activation_Softmax()

for _ in range(100):

    #Forward
    dense1.forward(X)
    activation1.forward(dense1.output)
    dense2.forward(activation1.output)
    activation2.forward(dense2.output)

    loss_function = Loss_CategoricalCrossentropy()
    loss = loss_function.calculate(activation2.output, y)

    print("Loss:", loss)

    #Backward
    dZ = activation2.output - y

    dense2.backward(dZ, learning_rate)
    activation1.backward()
    dZ = activation1.derivative * dense2.dA

    dense1.backward(dZ, learning_rate)