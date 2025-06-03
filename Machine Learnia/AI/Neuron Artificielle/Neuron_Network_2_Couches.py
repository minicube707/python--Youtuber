import numpy as np
from tqdm import tqdm
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from Neuron_Artificielle_Dog_VS_CAT_Corrigé import artificial_neuron, artificial_neuron2
from utilities import*

#Fonction
def initialisation(n0, n1, n2):
    W1 = np.random.randn(n1, n0)
    b1 = np.random.randn(n1, 1)
    W2 = np.random.randn(n2, n1)
    b2 = np.random.randn(n2, 1)

    parametres = {
        "W1" : W1,
        "b1" : b1,
        "W2" : W2,
        "b2" : b2
    }
    
    return parametres

def foward_propagation(X, parametres):

    W1 = parametres["W1"]
    b1 = parametres["b1"]
    W2 = parametres["W2"]
    b2 = parametres["b2"]

    Z1 = W1.dot(X) + b1
    A1 = 1/ (1 + np.exp(-Z1))
    Z2 = W2.dot(A1) + b2
    A2 = 1/ (1 + np.exp(-Z2))

    activation = {
        "A1" : A1,
        "A2" : A2
    }

    return activation

def back_propagation(activation, parametres, X, y):

    A1 = activation["A1"]
    A2 = activation["A2"]

    W2 = parametres["W2"]

    m = y.shape[1]

    dZ2 = A2 - y
    dW2 = 1/m * dZ2.dot(A1.T)
    db2 = 1/m * np.sum(dZ2, axis=1, keepdims=True)

    dZ1 = np.dot(W2.T, dZ2) * A1*(1-A1)
    dW1 = 1/m * dZ1.dot(X.T)
    db1 = 1/m * np.sum(dZ1, axis=1, keepdims=True)

    gradients = {
        "dW1" : dW1,
        "db1" : db1,
        "dW2" : dW2,
        "db2" : db2
    }

    return gradients    

def update(gradients, parametres, learning_rate):
    
    W1 = parametres["W1"]
    b1 = parametres["b1"]
    W2 = parametres["W2"]
    b2 = parametres["b2"]

    dW1 = gradients["dW1"]
    db1 = gradients["db1"]
    dW2 = gradients["dW2"]
    db2 = gradients["db2"]

    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2

    parametres = {
        "W1" : W1,
        "b1" : b1,
        "W2" : W2,
        "b2" : b2
    }
    
    return parametres

def predict(X, parametres):
    activations = foward_propagation(X, parametres)
    A2 = activations["A2"]
    return A2 >= 0.5

def log_loss(A, y):
    epsilon = 1e-15 #Pour empecher les log(0) = -inf
    return  1/y.size * np.sum( -y * np.log(A + epsilon) - (1-y)*np.log(1-A + epsilon))

#Network
def neural_network(X_train, y_train, n1, learning_rate=0.1, n_iteration=1000):

    n0 = X_train.shape[0]
    n2 = y_train.shape[0]
    #Initialisation
    parametres = initialisation(n0, n1, n2)

    train_loss = np.array([])
    train_accu = np.array([])

    for i in tqdm(range(n_iteration)):

        activation = foward_propagation(X_train, parametres)
        gradients = back_propagation(activation, parametres, X_train, y_train)
        parametres = update(gradients, parametres, learning_rate)

        if i%10 == 0:
            train_loss = np.append(train_loss, log_loss(activation["A2"], y_train))
            y_pred = predict(X_train, parametres)
            current_accuracy = accuracy_score(y_train.flatten(), y_pred.flatten()) #On applatit les données pour qu'elle ne soit pas rejeté par l'accuracy score
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
def neural_network2(X_train, y_train, X_test, y_test, n1, learning_rate=0.1, n_iteration=1000):

    n0 = X_train.shape[0]
    n2 = y_train.shape[0]
    #Initialisation
    parametres = initialisation(n0, n1, n2)

    train_loss = np.array([])
    train_accu = np.array([])
    test_loss = np.array([])
    test_accu = np.array([])

    for i in tqdm(range(n_iteration)):

        activation = foward_propagation(X_train, parametres)
        gradients = back_propagation(activation, parametres, X_train, y_train)
        parametres = update(gradients, parametres, learning_rate)

        if i%10 == 0:
            #Train
            train_loss = np.append(train_loss, log_loss(activation["A2"], y_train))
            y_pred = predict(X_train, parametres)
            current_accuracy = accuracy_score(y_train.flatten(), y_pred.flatten()) #On applatit les données pour qu'elle ne soit pas rejeté par l'accuracy score
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

if __name__ == "__Main__":

    #//////////////////////////////////////////////////////////////////////////
    #Dataset Circle
    X, y = make_circles(n_samples=100, noise=0.1, factor=0.3, random_state=0)
    y1 = y.reshape((y.shape[0], 1))
    X1 = X

    print("\nDimension de X1", X1.shape)
    print("Dimension de y1", y1.shape)

    plt.figure()
    plt.scatter(X1[:,0], X1[:,1], c=y1, cmap="winter")
    plt.title("Dataset")
    plt.show()

    print("\nTest du Dataset Circle sur un seul neuron\n")
    W, b = artificial_neuron(X1, y1, learning_rate=0.1, n_iteration=1000)

    x0 = np.linspace(X1[:,0].min(), X1[:,0].max(), 100)
    x1 = (-W[0] * x0 -b) / W[1]

    plt.figure()
    plt.scatter(X1[:,0], X1[:,1], c=y1, cmap="winter", label="Dataset")
    plt.plot(x0, x1, c="r", lw=3, label="Frontière de décision")
    plt.title("Dataset avec la fontière de décésion")
    plt.legend()
    plt.show()

    X2 = X1.T
    y2 = y1.T

    print("\nDimension de X2", X2.shape)
    print("Dimension de y2", y2.shape)

    print("\nTest du Dataset Cirlce sur un reseau de neuron\n")
    neural_network(X2, y2, 4, learning_rate=0.1, n_iteration=1000)


    #//////////////////////////////////////////////////////////////////////////
    #Dataset Dog VS Cat

    X_train, y_train, X_test, y_test = load_data()

    print("\nTrain")
    print("La dimension de X_train",X_train.shape)
    print("La dimension de y_train",y_train.shape)
    print(np.unique(y_train, return_counts=True))

    #Affichage des 10 premières images
    plt.figure(figsize=(16,8))
    for i in range(1,10):
        plt.subplot(4,5, i)
        plt.imshow(X_train[i], cmap="gray")
        plt.title(y_train[i])
        plt.tight_layout()
    plt.show()    

    #Nous avons redimensionner le X_train pour qu'ils ne contiennent que 1 varaiables (les 1000 échantillons et les 4096 pixels de notre image)
    #Nous avons ensuitenormaliser nos données en divisnant par le valeurs max du X_train

    X_train_reshape = X_train.reshape(X_train.shape[0], -1) / X_train.max()  
    print("La dimension de X_train_reshape",X_train_reshape.shape)

    X_test_reshape = X_test.reshape(X_test.shape[0], -1) / X_train.max()
    print("La dimension de X_test_reshape",X_test_reshape.shape)

    print("\nTest du Dataset DogCat sur un seul neuron\n")
    artificial_neuron2(X_train_reshape, y_train, X_test_reshape, y_test, learning_rate=0.01, n_iteration=8000)

    print("\nTest du Dataset DogCat sur un reseau de neuron\n")
    neural_network2(X_train_reshape.T, y_train.T, X_test_reshape.T, y_test.T, 32, learning_rate=0.01, n_iteration=8000)