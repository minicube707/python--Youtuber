
import  numpy                   as np
import  plotly.graph_objects    as go
import  matplotlib.pyplot       as plt
from    sklearn.datasets import make_blobs
from    sklearn.metrics  import accuracy_score


#Definition
def initialisation(X):
    W = np.random.randn(X.shape[1],1)
    b = np.random.randn(1)
    return (W,b)

def  Model(X, W, b):
    Z = X.dot(W) + b
    A = 1/(1 + np.exp(-Z))
    return A

def log_loss(A,y):
    return 1/len(y) * np.sum(-y*np.log(A)-(1-y)*np.log(1-A))

def gradient(A,X,y):
    dW= 1/len(y)*np.dot(X.T,A-y)
    db= 1/len(y)*np.sum(A-y)
    return (dW,db)

def uptade(dW,db,W,b,learning_rate):
    W = W-learning_rate*dW
    b = b-learning_rate*db
    return(W, b)

def  predict(X, W, b):
    A=Model(X, W, b)
    return A >=0.5 

def artificiel_neuron(X, y, learning_rate=0.1, nb_iteration=100):
    #initialisation W,b
    W,b =initialisation(X)

    Loss=[]

    for i in range(nb_iteration):
        A=Model(X, W, b)
        Loss.append(log_loss(A, y))
        dW, db=gradient(A, X, y)
        W, b=uptade(dW, db, W, b, learning_rate)

    y_predic= predict(X, W, b)
    print("La performance du neurone est ",accuracy_score(y, y_predic))

    plt.figure()
    plt.plot(Loss)
    plt.title("Courbe d'évolution du model")

    return (W, b)


#Main
X, y = make_blobs(n_samples=100, n_features=2, centers=2, random_state=0)
y=y.reshape((y.shape[0],1))

print('dimension de X', X.shape)
print('dimension de Y', y.shape)

plt.figure()
plt.scatter(X[:,0], X[:,1], c=y, cmap='summer', label="plante toxique")
plt.title("Configuration initial")
plt.legend()


W, b=initialisation(X)
print("w.shape=",W.shape)
print("w=",W)
print("b.shape=",b.shape)
print("b=",b)

A=Model(X,W,b)  
print("A.shape=",A.shape)

B=log_loss(A,y)
print("B=",B)

dW, db  =gradient(A,X,y)
print("db=",db)
print("db.shape=",db.shape)
print("dW=",dW)
print("dW.shape",dW.shape)

W,b =artificiel_neuron(X,y)

# Ajout d'un nouveau paramètre

new_plant=np.array([2,1])

#Calcul de l'affichage de la frontière de decision
x0= np.linspace(-1,4, 100)  # x0 s'étend de -1 à 4 avec 100 valeurs dans ce linspace 
x1= (-W[0]*x0-b)/W[1]       #Formule Mathématique tiré à partir de la combinaison linéaire du neurone W[0]*x0 + W[1]*x1 + b = 0

plt.figure()
plt.scatter(X[:,0], X[:,1], c=y, cmap='summer', label="plante toxique")
plt.scatter(new_plant[0], new_plant[1], c='b', label="Nouvelle plante")
plt.plot(x0, x1, c='r', label="Frontière de décision")
plt.legend()
plt.show()
C=predict(new_plant, W, b)
print(C)
if C== True:
    print("La nouvelle plante est toxique")
else:
    print("La nouvelle plante n'est pas toxique")


#Visualisation 3D
fig = go.Figure(data=[go.Scatter3d( 
    x=X[:, 0].flatten(),
    y=X[:, 1].flatten(),
    z=y.flatten(),
    mode='markers',
    marker=dict(
        size=5,
        color=y.flatten(),                
        colorscale='YlGn',  
        opacity=0.8,
        reversescale=True
    )
)])

fig.update_layout(template= "plotly_dark", margin=dict(l=0, r=0, b=0, t=0))
fig.layout.scene.camera.projection.type = "orthographic"
fig.show()

X0 = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)
X1 = np.linspace(X[:, 1].min(), X[:, 1].max(), 100)
xx0, xx1 = np.meshgrid(X0, X1)
Z = W[0] * xx0 + W[1] * xx1 + b
A = 1 / (1 + np.exp(-Z))

fig = (go.Figure(data=[go.Surface(z=A, x=xx0, y=xx1, colorscale='YlGn', opacity = 0.7, reversescale=True)]))

fig.add_scatter3d(x=X[:, 0].flatten(), y=X[:, 1].flatten(), z=y.flatten(), mode='markers', marker=dict(size=5, color=y.flatten(), colorscale='YlGn', opacity = 0.9, reversescale=True))


fig.update_layout(template= "plotly_dark", margin=dict(l=0, r=0, b=0, t=0))
fig.layout.scene.camera.projection.type = "orthographic"
fig.show()


