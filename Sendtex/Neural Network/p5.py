import numpy as np

np.random.seed(0)

X  = [[1, 2, 3, 2.5],
    [2.0, 5.0, -1.0, 2.0],
    [-1.5, 2.7, 3.3, -0.8]]


inputs = [0, 2, -1, 3.3, -2.7, 1.1, 2.2, -100]
outputs = []


#RELU
for i in inputs:
    if i > 0:
        outputs.append(i)
    else:
        outputs.append(0)

print(outputs)


class Layer_Dense:

    def __init__(self, n_inputs, n_neurons):
        self.weights = np.random.randn(n_inputs, n_neurons) * 0.1
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output =  np.dot(inputs, self.weights) + self.biases

class Activation_Relu:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

layer1 = Layer_Dense(4, 5)
layer2 = Layer_Dense(5, 2)

print("\nLayer1")
layer1.forward(X)
print(layer1.output)

print("\nLayer2")
layer2.forward(layer1.output)
print(layer2.output)