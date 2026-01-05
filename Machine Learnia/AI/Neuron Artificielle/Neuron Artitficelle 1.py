import  numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.metrics import accuracy_score

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
    return  1/y.size * np.sum( -y*np.log(A) - (1-y)*np.log(1-A))

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
    print(A)
    return A>= 0.5

#Main
X, y = make_blobs(n_samples=100, n_features=2, centers=2, random_state=0)
y = y.reshape((y.shape[0],1))

print("Dimension de X", X.shape)
print("Dimension de y ", y.shape)

plt.figure()
plt.scatter(X[:,0], X[:,1], c=y, cmap="winter")
plt.title("Dataset")
plt.show()

#Test 

#Initialisation
print("")
W, b = initialisation(X)
print("Dimension de W", W.shape)
print("W =",W)
print("Dimension de b ", b.shape)
print("b =",b)

#Model
print("")
A = model(X, W, b)
print("Dimension de A ", A.shape)
print("A =",A)

#Log_Loss
print("")
l = log_loss(A, y)
print("l =",l)

#Gradients
print("")
dW, db = gradients(A, X, y)
print("Dimension de dW ", dW.shape)
print("dW =",dW)
print("db =",db)

#Update
print("")
learning_rate = 0.5
W, b = update(dW, db, W, b, learning_rate)
print("Dimension de dW ", dW.shape)
print("dW =",W)
print("db =",b)

#Neuron artificielle
def artificial_neuron(X, y, learning_rate= 0.1, n_iteration= 100):
    #Initialisation
    W, b = initialisation(X)
    loss = np.array([])

    for i in range(n_iteration):
        A = model(X, W, b)
        loss = np.append(loss, log_loss(A, y))
        dW, db = gradients(A, X, y)
        W, b = update(dW, db, W, b, learning_rate)

    y_predict = predict(X, W, b)
    print("L'accuracy est de ",accuracy_score(y, y_predict))

    plt.figure()
    plt.plot(np.arange(loss.size), loss)
    plt.title("Fonction Cout")
    plt.show()

    return (W, b)

W, b = artificial_neuron(X, y)

new_plant = np.array([2, 1])

x0 = np.linspace(-1, 4, 100)
x1 = (-W[0] * x0 -b) / W[1]

plt.figure()
plt.scatter(X[:,0], X[:,1], c=y, cmap="winter", label="Dataset")
plt.scatter(new_plant[0], new_plant[1], c='r', label="Nouvelle Plantes")
plt.plot(x0, x1, c="orange", lw=3, label="Frontière de décision")
plt.title("New Plant")
plt.legend()
plt.show()

dangerous = predict(new_plant, W, b)
if dangerous == True:
    print("La plante est toxique")
else:
    print("La plante n'est pas toxique")