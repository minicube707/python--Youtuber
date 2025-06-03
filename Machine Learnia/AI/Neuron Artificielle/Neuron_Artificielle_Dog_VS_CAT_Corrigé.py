import  numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from utilities import*
from tqdm import tqdm

#Fonction
def initialisation(X):
    W = np.random.randn(X.shape[1], 1)
    b = np.random.randn(1)

    return W, b

def model(X, W, b):
    Z =X.dot(W) +b
    A = 1/ (1 + np.exp(-Z))

    return A

def log_loss(A, y):
    epsilon = 1e-15 #Pour empecher les log(0) = -inf
    return  1/y.size * np.sum( -y*np.log(A + epsilon) - (1-y)*np.log(1-A + epsilon))

def gradients(A, X, y):
    dW = 1/y.size * np.dot(X.T, A-y)
    db = 1/y.size * np.sum(A-y)
    return (dW, db)

def update(dW, db, W, b, learning_rate):
    W = W - learning_rate*dW
    b = b - learning_rate*db
    return (W, b)

def predict(X, W, b):
    A = model(X, W, b)
    return A>= 0.5

#Neuron artificielle
def artificial_neuron(X_train, y_train, learning_rate= 0.1, n_iteration= 100):
    #Initialisation
    W, b = initialisation(X_train)

    train_loss = np.array([])
    train_acc = np.array([])

    for i in tqdm(range(n_iteration)):

        #Model
        A = model(X_train, W, b)

        if i%10 == 0:

            #Train
            #Calcul Cost function
            train_loss = np.append(train_loss, log_loss(A, y_train))

            #Calcul de l'accuracy
            y_predict = predict(X_train, W, b)
            train_acc = np.append(train_acc, accuracy_score(y_train, y_predict))

        #Mise à jour
        dW, db = gradients(A, X_train, y_train)
        W, b = update(dW, db, W, b, learning_rate)

    print("L'accuracy final du train_set est de ",train_acc[-1])

    plt.figure(figsize=(12,4))
    plt.subplot(1, 2, 1)
    plt.plot(train_loss, label="Cost function du train_set")
    plt.title("Fonction Cout en fonction des itérations")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(train_acc, label="Accuracy du train-set")
    plt.title("\nL'acccuracy en fonction des itérations")
    plt.legend()
    plt.show()

    return (W, b)

#Neuron artificielle2
def artificial_neuron2(X_train, y_train, X_test, y_test, learning_rate= 0.1, n_iteration= 100):
    #Initialisation
    W, b = initialisation(X_train)

    train_loss = np.array([])
    train_acc = np.array([])
    test_loss = np.array([])
    test_acc = np.array([])


    for i in tqdm(range(n_iteration)):

        #Model
        A = model(X_train, W, b)

        if i%10 == 0:

            #Train
            #Calcul Cost function
            train_loss = np.append(train_loss, log_loss(A, y_train))

            #Calcul de l'accuracy
            y_predict = predict(X_train, W, b)
            train_acc = np.append(train_acc, accuracy_score(y_train, y_predict))

            #Test
            #Calcul Cost function
            A_test = model(X_test, W, b)
            test_loss = np.append(test_loss, log_loss(A_test, y_test))

            #Calcul de l'accuracy
            y_predict = predict(X_test, W, b)
            test_acc = np.append(test_acc, accuracy_score(y_test, y_predict))

        #Mise à jour
        dW, db = gradients(A, X_train, y_train)
        W, b = update(dW, db, W, b, learning_rate)

    print("L'accuracy final du train_set est de ",train_acc[-1])
    print("L'accuracy final du test_set est de ",test_acc[-1])

    plt.figure(figsize=(12,4))
    plt.subplot(1, 2, 1)
    plt.plot(train_loss, label="Cost function du train_set")
    plt.plot(test_loss, label="Cost function du test_set")
    plt.title("Fonction Cout en fonction des itérations")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(train_acc, label="Accuracy du train-set")
    plt.plot(test_acc, label="Accuracy du test_set")
    plt.title("L'acccuracy en fonction des itérations")
    plt.legend()
    plt.show()

    return (W, b)

if __name__ =="__main__":

    #Main
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

    #Nous avons redimensionner le X_train pour qu'ils ne contiennent que 1 varaiables (les 1000 échantillons et les 4096 pixels de notre image)
    #Nous avons ensuitenormaliser nos données en divisnant par le valeurs max du X_train
    X_train_reshape = X_train.reshape(X_train.shape[0], -1) / X_train.max()  
    print("La dimension de X_train_reshape",X_train_reshape.shape)

    X_test_reshape = X_test.reshape(X_test.shape[0], -1) / X_train.max()
    print("La dimension de X_test_reshape",X_test_reshape.shape)

    W, b = artificial_neuron2(X_train_reshape, y_train, X_test_reshape, y_test, learning_rate=0.01, n_iteration=10_000)
    print("\nDimension de W", W.shape)
    print("W =",W)
    print("Dimension de b ", b.shape)
    print("b =",b)

    #Bonus Perso: Affichage des poids
    W_reshape = W.reshape(X_train.shape[1], X_train.shape[2])
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