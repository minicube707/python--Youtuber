import numpy as np
from tqdm import tqdm
from utilities import*

from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt


#Fonction
#Neuron
def initialisation(dimension):

    parametres ={}

    parametres["W1"] = np.random.randn(dimension[1], dimension[0])
    parametres["b1"] = np.random.randn(dimension[1], 1)

    parametres["W2"] = np.random.randn(dimension[2], dimension[1])
    parametres["b2"] = np.random.randn(dimension[2], 1)

    return parametres

def add_dimension(old_parametre, layer, previouus_layer):

    c = len(old_parametre) // 2

    old_parametre["W" + str(c+1)] = old_parametre["W" + str(c)]
    old_parametre["b" + str(c+1)] = old_parametre["b" + str(c)]

    old_parametre["W" + str(c)] = np.random.randn(layer, previouus_layer)
    old_parametre["b" + str(c)] = np.random.randn(layer, 1)

    return old_parametre

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
    Af =activations["A" + str(C)]
    return Af >= 0.5

def log_loss(A, y):
    epsilon = 1e-15 #Pour empecher les log(0) = -inf
    return  1/y.size * np.sum( -y * np.log(A + epsilon) - (1-y)*np.log(1-A + epsilon))


#Network
def deep_neural_network_update1(X_train, y_train, X_test, y_test, hidden_layer, learning_rate=0.1, n_iteration=1000):

    np.random.seed(0)
    list_cut = np.floor(np.linspace(0, n_iteration, len(hidden_layer)+1)).astype(int)
    index = 1

    #Initialisation
    dimensions = []
    
    dimensions.insert(0, X_train.shape[0])
    dimensions.append(hidden_layer[0])
    dimensions.append(y_train.shape[0])

    parametres = initialisation(dimensions) 

    train_loss = np.array([])
    train_accu = np.array([])
    test_loss = np.array([])
    test_accu = np.array([])

    for i in tqdm(range(n_iteration)):

        if i == list_cut[index]:

            print("\nnew parametre")

            new_dimensions = list(hidden_layer)[index]
            old_dimension = list(hidden_layer)[index-1]
            parametres = add_dimension(parametres, new_dimensions, old_dimension)
            for key, val in parametres.items():
                print(key, val.shape)

            index += 1

        activation = foward_propagation(X_train, parametres)
        gradients = back_propagation(activation, parametres, y_train)
        parametres = update(gradients, parametres, learning_rate)

        if i % 50 == 0:

            #Train
            train_loss = np.append(train_loss, log_loss(activation["A2"], y_train))
            y_pred = predict(X_train, parametres)
            current_accuracy = accuracy_score(y_train.flatten(), y_pred.flatten()) 
            train_accu = np.append(train_accu, current_accuracy)

            #Test
            test_activation = foward_propagation(X_test, parametres)

            test_loss = np.append(test_loss, log_loss(test_activation["A2"], y_test))
            y_pred = predict(X_test, parametres)
            current_accuracy = accuracy_score(y_test.flatten(), y_pred.flatten()) 
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

#Graph
def reshape_to_square(arr):
    total_elements = arr.size
    square_dim = int(np.sqrt(total_elements))

    for i in range(square_dim, 0, -1):
        if total_elements % i == 0:
            return arr.reshape((i, -1))

    # Si on ne peut pas obtenir une forme carrée, simplement réorganiser avec la dimension trouvée
    return arr.reshape((square_dim, -1))

#//////////////////////////////////////////////////////////////////////////
#Test
print("\nTest")

X = np.array([[0], [1]])
y = np.array([[1]])

print("\ninitialisation")
parametres = initialisation([2, 32, 1])
for key, val in parametres.items():
    print(key, val.shape)
print(len(parametres))

print("\nadd_layer")
parametres = add_dimension(parametres , 32, 32)
for key, val in parametres.items():
    print(key, val.shape)

print("\nforward propagation")
activation = foward_propagation(X, parametres)
for key, val in activation.items():
    print(key, val.shape)

print("\nbackward propagation")
gradiant = back_propagation(activation, parametres, y)
for key, val in gradiant.items():
    print(key, val.shape)

#//////////////////////////////////////////////////////////////////////////
#Data_Digit
    

digits =load_digits()

images = digits.images
X= digits.data
y= digits.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=5)

y_train = y_train.reshape((y_train.shape[0], 1))
y_test = y_test.reshape((y_test.shape[0], 1))

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
    plt.imshow(X_train.reshape((X_train.shape[0], 8, 8))[i], cmap="gray")
    plt.title(y_train[i])
    plt.tight_layout()
plt.show()    

New_X_train = X_train.T / X_train.max()  
New_X_test = X_test.T / X_train.max()

y_test = y_test.T
y_train = y_train.T

#Pour les X se sont les variables en premier (ici les pixels) puis le nombres d'échantillons 
#Pour les y se sont les labels d'abord puis le nombre d'échantillons
print("\nNew_X_train.shape:", New_X_train.shape)
print("New_X_test.shape:", New_X_test.shape)
print("y_test.shape:", y_test.shape)
print("y_train.shape:", y_train.shape)


#Data DogCat
"""
X_train, y_train, X_test, y_test = load_data()

y_train = y_train.reshape((y_train.shape[0], 1))
y_test = y_test.reshape((y_test.shape[0], 1))

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

New_X_train = X_train.reshape(X_train.shape[0], -1) / X_train.max()  
New_X_test = X_test.reshape(X_test.shape[0], -1) / X_train.max()

New_X_test = New_X_test.T
New_X_train = New_X_train.T

y_test = y_test.T
y_train = y_train.T

#Pour les X se sont les variables en premier (ici les pixels) puis le nombres d'échantillons 
#Pour les y se sont les labels d'abord puis le nombre d'échantillons
print("\nNew_X_train.shape:", New_X_train.shape)
print("New_X_test.shape:", New_X_test.shape)
print("y_test.shape:", y_test.shape)
print("y_train.shape:", y_train.shape)
"""
#//////////////////////////////////////////////////////////////////////////
#Model

print("")
parametres = deep_neural_network_update1(New_X_train, y_train, New_X_test, y_test, (64, 64, 64, 64, 64), learning_rate=0.01, n_iteration=20_000)
#La meilleure performance de l'accurancy score est 1

print("")
for key, val in parametres.items():
    print(key, val.shape)

key1 = list(parametres.keys())[-1]
key2 = list(parametres.keys())[-2]

W = parametres[key2]
b = parametres[key1]

#Bonus Perso: Affichage des poids
W_reshape = reshape_to_square(W)

#Graphique
plt.figure()
plt.imshow(W_reshape)
plt.title("Model")
plt.tight_layout()
plt.colorbar()
plt.show()
