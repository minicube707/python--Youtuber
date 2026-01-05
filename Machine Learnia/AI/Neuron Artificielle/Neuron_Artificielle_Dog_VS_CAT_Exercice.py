import  numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, log_loss
from sklearn.preprocessing import MinMaxScaler
from utilities import*

#Fonction
def initialisation(X):
    W = np.random.randn(X.shape[1], 1)
    b = np.random.randn(1)

    return W, b

def model(X, W, b):
    Z =X.dot(W) +b
    A = 1/ (1 + np.exp(-Z))

    return A

def Log_loss(A, y):
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
    return A>= 0.5

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

plt.figure(figsize=(16,8))
for i in range(1,10):
    plt.subplot(4,5, i)
    plt.imshow(X_train[i], cmap="gray")
    plt.title(y_train[i])
    plt.tight_layout()
plt.show()    

X_train_nor = np.array([])
for i in range(X_train.shape[0]):
    transformer = MinMaxScaler()
    X = transformer.fit_transform(X_train[i,:,:])
    X_train_nor = np.append(X_train_nor, np.array([X]))

X_train_nor = X_train_nor.reshape(X_train.shape[0],-1)
print("\n La dimension de X_train_nor",X_train_nor.shape)


#Initialisation
print("")
W, b = initialisation(X_train_nor)
print("Dimension de W", W.shape)
print("W =",W)
print("Dimension de b ", b.shape)
print("b =",b)

#Model
print("")
A = model(X_train_nor, W, b)
print("Dimension de A ", A.shape)

#Log_Loss
print("")
l = log_loss(y_train, A)
print("log_loss =",l)

#Gradients
print("")
dW, db = gradients(A, X_train_nor, y_train)
print("Dimension de dW ", dW.shape)
print("dW =",dW)
print("db =",db)

#Update
print("")
learning_rate = 0.5
dW, db = update(dW, db, W, b, learning_rate)
print("Dimension de dW ", dW.shape)
print("dW =",dW)
print("db =",db)

#Neuron artificielle
def artificial_neuron(X_train_nor, y_train, learning_rate= 0.01, n_iteration= 1000):
    #Initialisation
    W, b = initialisation(X_train_nor)
    loss = np.array([])

    for _ in range(n_iteration):
        A = model(X_train_nor, W, b)
        loss = np.append(loss, log_loss(y_train, A))
        dW, db = gradients(A, X_train_nor, y_train)
        W, b = update(dW, db, W, b, learning_rate)

    y_predict = predict(X_train_nor, W, b)
    print("L'accuracy est de ",accuracy_score(y_train, y_predict))

    plt.figure()
    plt.plot(np.arange(loss.size), loss)
    plt.title("Fonction Cout du train")
    plt.show()

    return (W, b)

if __name__ =="__main__":

    W, b = artificial_neuron(X_train_nor, y_train)
    
    
    X_test_nor = np.array([])
    for i in range(X_test.shape[0]):
        transformer = MinMaxScaler()
        X = transformer.fit_transform(X_test[i,:,:])
        X_test_nor = np.append(X_test_nor, np.array([X]))
    
    X_test_nor = X_test_nor.reshape(X_test.shape[0],-1)
    print("\n La dimension de X_test_nor",X_test_nor.shape)
    loss = np.array([])
    
    for _ in range(y_test.size):
            
        A = model(X_test_nor, W, b)
        loss = np.append(loss, log_loss(y_test, A))
        dW, db = gradients(A, X_test_nor, y_test)
        W, b = update(dW, db, W, b, learning_rate= 0.01)
    
    y_predict = predict(X_test_nor, W, b)
    print("L'accuracy du test est de ",accuracy_score(y_test, y_predict))
    
    plt.figure()
    plt.plot(np.arange(loss.size), loss)
    plt.title("Fonction Cout test set")
    plt.show()