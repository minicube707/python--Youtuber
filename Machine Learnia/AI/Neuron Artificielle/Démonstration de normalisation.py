import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import plotly.graph_objects as go

plt.style.use('dark_background')
plt.rcParams.update({
    "figure.facecolor":  (0.12 , 0.12, 0.12, 1),
    "axes.facecolor": (0.12 , 0.12, 0.12, 1),
})

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

def artificial_neuron_2(X, y, learning_rate=0.1, n_iter=1000):

    W, b = initialisation(X)
    W[0], W[1] = -7.5, 7.5

    nb = 1
    j=0
    history = np.zeros((n_iter // nb, 5))

    A = model(X, W, b)
    Loss = []
    

    Params1 = [W[0]]
    Params2 = [W[1]]
    Loss.append(log_loss(y, A))
    
    # Training
    for i in range(n_iter):
      A = model(X, W, b)
      Loss.append(log_loss(y, A))
      Params1.append(W[0])
      Params2.append(W[1])
      dW, db = gradients(A, X, y)
      W, b = update(dW, db, W, b, learning_rate = learning_rate)

      if (i % nb == 0):  
        history[j, 0] = float(W[0])
        history[j, 1] = float(W[1])
        history[j, 2] = float(b)
        history[j, 3] = i
        history[j, 4] = log_loss(y, A)
        j +=1
    
    plt.figure()
    plt.plot(np.arange(len(Loss)), Loss)
    plt.title("Loss en fonction des itérations")
    plt.show()

    return history, b, Loss, Params1, Params2

X, y = make_blobs(n_samples=100, n_features=2, centers=2, random_state=0)
X[:,1] = X[:,1]*1
y = y.reshape((y.shape[0],1))

print("Dimension de X", X.shape)
print("Dimension de y ", y.shape)

plt.figure()
plt.scatter(X[:,0], X[:,1], c=y, cmap="winter")
plt.title("Dataset")
plt.show()


lim = 10
h = 100
W1 = np.linspace(-lim, lim, h)
W2 = np.linspace(-lim, lim, h)
#W1 et W2 sont deux lines allant de -lim à lim avec h graduation

W11, W22 = np.meshgrid(W1, W2)
#W11 et W22 sont deux grilles de valeur

W_final = np.c_[W11.ravel(), W22.ravel()].T
print("La Dimension de W_final est de ",W_final.shape)
#W_final est un tableau de configuration contenant 10 000 configurations

#Model
b=0
Z = X.dot(W_final) + b
A = 1/(1 + np.exp(-Z))
print("La Dimension de A est de ",A.shape)

#Log_loss
epsilon = 1e-15 #Pour empecher les log(0) = -inf
L = 1/y.size * np.sum( -y*np.log(A + epsilon) - (1-y)*np.log(1-A + epsilon), axis=0).reshape(W11.shape)
print("La Dimension de L est de ",L.shape)

#Graphique
plt.figure()
plt.contourf(W11, W22, L, cmap="magma")
plt.colorbar()
plt.xlabel("W11")
plt.ylabel("W22")
plt.title("Loss en fonction de W11 et W22")
plt.show()


history, b, Loss, Params1, Params2 = artificial_neuron_2(X, y, learning_rate=0.6, n_iter=100)

def animate(params):
    W0 = params[0]
    W1 = params[1]
    b = params[2]
    i = params[3]
    loss = params[4]
    

    #ax[0].clear() # frontiere de décision
    #ax[1].clear() # sigmoide
    #ax[2].clear() # fonction Cout
    
    ax[0].contourf(W11, W22, L, 20, cmap='magma', zorder=-1)
    ax[0].scatter(Params1[int(i)], Params2[int(i)], c='r', marker='x', s=50, zorder=1)
    ax[0].plot(Params1[0:int(i)], Params2[0:int(i)], lw=3, c='r', zorder=1)

    ax[1].plot(Loss[0:int(i)], lw=3, c='r')
    ax[1].set_xlim(0, len(Params1))
    ax[1].set_ylim(min(Loss) - 2, max(Loss) + 2)

#Graphique 1
#Graphique de la decente de gradient
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.contourf(W11, W22, L, 10, cmap='magma')
plt.title("Loss en fonction de W11 et W22")
plt.colorbar()

#Graphique de la decente de gradient avec le chemin
plt.subplot(1, 2, 2)
plt.contourf(W11, W22, L, 10, cmap='magma')
plt.scatter(history[:, 0], history[:, 1], c=history[:, 2], cmap='Blues', marker='x')
plt.plot(history[:, 0], history[:, 1])
plt.plot(history[:, 0], history[:, 1], c='r')
plt.colorbar()
plt.title("Loss en fonction de W11 et W22 avec le suivi du gradient")
plt.show()

print("\nVeuilliez patienter que le programme termine ses calcul !!!")
print("Cela peut prendre 1 à 2 minutes")


#Animation
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 10))
ani = FuncAnimation(fig, animate, frames=history, interval=10, repeat=False)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=3200)
ani.save('animation3.mp4', writer=writer)



fig = (go.Figure(data=[go.Surface(z=L, x=W11, y=W22, opacity = 1)]))

fig.update_layout(template= "plotly_dark", margin=dict(l=0, r=0, b=0, t=0))
fig.layout.scene.camera.projection.type = "orthographic"
fig.show()

