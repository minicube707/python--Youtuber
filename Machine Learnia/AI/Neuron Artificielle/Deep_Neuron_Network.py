import numpy as np
from tqdm import tqdm
from utilities import*

from sklearn.datasets import make_circles
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt

from Neuron_Artificielle_Dog_VS_CAT_Corrigé import artificial_neuron2
from Neuron_Network_2_Couches import neural_network2


#Fonction
def initialisation(dimension):

    parametres ={}
    C = len(dimension)

    for c in range(1, C):
        parametres["W" + str(c)] = np.random.randn(dimension[c], dimension[c-1])
        parametres["b" + str(c)] = np.random.randn(dimension[c], 1)

    return parametres

def foward_propagation(X, parametres):

    activation = {"A0" : X}

    C =len(parametres) // 2

    for c in range(1, C+1):
        Z = parametres["W" + str(c)].dot(activation["A" + str(c-1)]) + parametres["b" + str(c)]
        activation["A" + str(c)] = 1 / (1 + np.exp(-Z))

    return activation

def back_propagation(activation, parametres, y):

    m = y.shape[1]
    C = len(parametres) // 2

    dZ = activation["A" + str(C)] - y
    gradients = {}

    for c in reversed(range(1, C+1)):
        gradients["dW" + str(c)] = 1/m * np.dot(dZ, activation["A" + str(c-1)].T)
        gradients["db" + str(c)] = 1/m * np.sum(dZ, axis=1, keepdims=True)
        
        if c > 1:
            dZ = np.dot(parametres["W" + str(c)].T, dZ) * activation["A" + str(c-1)] * (1 - activation["A" + str(c-1)])

    return gradients    

def update(gradients, parametres, learning_rate):
    
    C = len(parametres) // 2

    for c in range(1, C+1):
        parametres["W" + str(c)] = parametres["W" + str(c)] - learning_rate * gradients["dW" + str(c)]
        parametres["b" + str(c)] = parametres["b" + str(c)] - learning_rate * gradients["db" + str(c)]
    
    return parametres

def predict(X, parametres):
    activations = foward_propagation(X, parametres)
    C = len(parametres) // 2
    Af = activations["A" + str(C)]
    return Af >= 0.5

def log_loss(A, y):
    epsilon = 1e-15 #Pour empecher les log(0) = -inf
    return  1/y.size * np.sum( -y * np.log(A + epsilon) - (1-y)*np.log(1-A + epsilon))

#Network
def deep_neural_network(X, y, hidden_layer, learning_rate=0.1, n_iteration=1000):

    np.random.seed(0)
    #Initialisation
    dimensions = list(hidden_layer)
    dimensions.insert(0, X.shape[0])
    dimensions.append(y.shape[0])
    parametres = initialisation(dimensions)

    train_loss = np.array([])
    train_accu = np.array([])

    for i in tqdm(range(n_iteration)):

        activation = foward_propagation(X, parametres)
        gradients = back_propagation(activation, parametres, y)
        parametres = update(gradients, parametres, learning_rate)

        if i%10 == 0:
            train_loss = np.append(train_loss, log_loss(activation["A2"], y))
            y_pred = predict(X, parametres)
            current_accuracy = accuracy_score(y.flatten(), y_pred.flatten()) 
            train_accu = np.append(train_accu, current_accuracy)

    print("L'accuracy final du train_set est de ",train_accu[-1])

    plt.figure(figsize=(12,4))
    plt.subplot(1, 2, 1)
    plt.plot(train_loss, label="Cost function du train_set")
    plt.title("Fonction Cout en fonction des itérations")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(train_accu, label="Accuracy du train_set")
    plt.title("L'acccuracy en fonction des itérations")
    plt.legend()
    plt.show()

    return parametres

#Network2
def deep_neural_network2(X_train, y_train, X_test, y_test, hidden_layer, learning_rate=0.1, n_iteration=1000):

    np.random.seed(0)
    #Initialisation
    dimensions = list(hidden_layer)
    dimensions.insert(0, X_train.shape[0])
    dimensions.append(y_train.shape[0])
    parametres = initialisation(dimensions)

    train_loss = np.array([])
    train_accu = np.array([])
    test_loss = np.array([])
    test_accu = np.array([])

    for i in tqdm(range(n_iteration)):

        activation = foward_propagation(X_train, parametres)
        gradients = back_propagation(activation, parametres, y_train)
        parametres = update(gradients, parametres, learning_rate)

        if i%10 == 0:
            #Train
            train_loss = np.append(train_loss, log_loss(activation["A2"], y_train))
            y_pred = predict(X_train, parametres)
            current_accuracy = accuracy_score(y_train.flatten(), y_pred.flatten()) 
            train_accu = np.append(train_accu, current_accuracy)

            #Test
            test_activation = foward_propagation(X_test, parametres)

            test_loss = np.append(test_loss, log_loss(test_activation["A2"], y_test))
            y_pred = predict(X_test, parametres)
            current_accuracy = accuracy_score(y_test.flatten(), y_pred.flatten()) #On applatit les données pour qu'elle ne soit pas rejeté par l'accuracy score
            test_accu = np.append(test_accu, current_accuracy)

    print("L'accuracy final du train_set est de ",train_accu[-1])
    print("L'accuracy final du test_set est de ",test_accu[-1])

    plt.figure(figsize=(12,4))
    plt.subplot(1, 2, 1)
    plt.plot(train_loss, label="Cost function du train_set")
    plt.plot(test_loss, label="Cost function du test_set")
    plt.title("Fonction Cout en fonction des itérations")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(train_accu, label="Accuracy du train_set")
    plt.plot(test_accu, label="Accuracy du test_set")
    plt.title("L'acccuracy en fonction des itérations")
    plt.legend()
    plt.show()

    return parametres

#//////////////////////////////////////////////////////////////////////////
#Test
print("\nTest")

X = np.array([[0], [1]])
y = np.array([[1]])

print("\ninitialisation")
parametres = initialisation([2, 32, 32, 12, 1])
for key, val in parametres.items():
    print(key, val.shape)
print(len(parametres))

print("\nforward propagation")
activation = foward_propagation(X, parametres)
for key, val in activation.items():
    print(key, val.shape)

print("\nbackward propagation")
gradiant = back_propagation(activation, parametres, y)
for key, val in gradiant.items():
    print(key, val.shape)

#//////////////////////////////////////////////////////////////////////////
#Dataset Circle
X, y = make_circles(n_samples=100, noise=0.1, factor=0.3, random_state=0)
y = y.reshape((1,y.shape[0]))
X = X.T

deep_neural_network(X, y, (32, 32, 32), 0.1, 1000)

plt.figure()
plt.scatter(X[0], X[1], c=y)
plt.show()

#//////////////////////////////////////////////////////////////////////////
#Dataset DogCat
X_train, y_train, X_test, y_test = load_data()

print("\nTrain")
print("La dimension de X_train",X_train.shape)
print("La dimension de y_train",y_train.shape)
print(np.unique(y_train, return_counts=True))

print("\nTest")
print("La dimension de X_test",X_test.shape)
print("La dimension de y_test",y_test.shape)
print(np.unique(y_test, return_counts=True))

#Affichage des 10 premières images
plt.figure(figsize=(16,8))
for i in range(1,10):
    plt.subplot(4,5, i)
    plt.imshow(X_train[i], cmap="gray")
    plt.title(y_train[i])
    plt.tight_layout()
plt.show()    

X_train_reshape = X_train.reshape(X_train.shape[0], -1) / X_train.max()  
X_test_reshape = X_test.reshape(X_test.shape[0], -1) / X_train.max()

#Pour les X se sont les variables en premier (ici les pixels) puis le nombres d'échantillons 
#Pour les y se sont les labels d'abord puis le nombre d'échantillons
print("\nLa dimension de X_train_reshape",X_train_reshape.shape)
print("La dimension de X_test_reshape",X_test_reshape.shape)

#//////////////////////////////////////////////////////////////////////////
#Model

print("\nTest du Dataset DogCat sur un seul neuron\n")
artificial_neuron2(X_train_reshape, y_train, X_test_reshape, y_test, learning_rate=0.01, n_iteration=8000)

print("\nTest du Dataset DogCat sur un reseau de neuron\n")
neural_network2(X_train_reshape.T, y_train.T, X_test_reshape.T, y_test.T, 32, learning_rate=0.01, n_iteration=8000)


print("\nTest du Dataset DogCat sur un reseau de neuron profond\n")
parametres = deep_neural_network2(X_train_reshape.T, y_train.T, X_test_reshape.T, y_test.T, (32, 32, 32), learning_rate=0.01, n_iteration=8000)
"""
for key, val in parametres.items():
    print(key, val.shape)

W = parametres["W4"]
b = parametres["b4"]

print("\nDimension de W", W.shape)
print("W =",W)
print("Dimension de b ", b.shape)
print("b =",b)

#Bonus Perso: Affichage des poids
W_reshape = W.reshape((4, -1))
print("\nDimension de W_reshape", W_reshape.shape)
print("W_reshape =",W_reshape)
print("Dimension de b ", b.shape)
print("b =",b)

#Graphique
plt.figure()
plt.imshow(W_reshape)
plt.title("Model")
plt.tight_layout()
plt.colorbar()
plt.show()
"""