import math
import numpy as np

#Original code
print("Original code")

E = 2.71828182846

layer_output =  [4.8, 1.21, 2.385]

exp_values = []
for output in layer_output:
    exp_values.append(E**output)

print(exp_values)

norm_base = sum(exp_values)
norm_value = []

for value in exp_values:
    norm_value.append(value / norm_base)

print(norm_value)
print(sum(norm_value))


#Numpy code1
print("\nNumpy code2")
layer_output =  [[4.8, 1.21, 2.385],
                 [8.9, -1.81, 0.2], 
                 [1.41, 1.051, 0.026]]

exp_values = np.exp(layer_output)
print(exp_values)

norm_value = exp_values / np.sum(exp_values)
print(norm_value)
print(np.sum(norm_value))
print(np.sum(layer_output, axis=1, keepdims=True))


#Numpy code2
print("\nNumpy code2")
layer_output =  [[4.8, 1.21, 2.385],
                 [8.9, -1.81, 0.2], 
                 [1.41, 1.051, 0.026]]

exp_values = np.exp(layer_output)
norm_value = exp_values / np.sum(exp_values, axis=1, keepdims=True)
print(norm_value)