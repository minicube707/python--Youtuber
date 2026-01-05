
import numpy as np
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt

# Defintion

#Model
def Model (X,theta):
    return X.dot(theta)

#Fonction cout
def cost_function(X, y, theta):
    return 1/(2*len(y))*np.sum((Model(X, theta)-y)**2)

# Gradient et descente de Gradient
def grad(X, y, theta):
    return 1/len(y)*X.T.dot(Model(X,theta)-y)

def gradient_descent(X, y, theta, learning_rate, nb_iteration):

    cost_history=np.zeros(nb_iteration)

    for i in range(0,nb_iteration):
        print(grad(X, y, theta))
        theta=theta-learning_rate*grad(X, y, theta)
        cost_history[i]=cost_function(X,y,theta)

    return theta, cost_history

def coef_determaination(y,prediction):
    u=((y-prediction)**2).sum()
    v=((y-y.mean())**2).sum()
    return 1-u/v

#Main
plt.figure()
np.random.seed(0) # pour produire toujours le meme vecteur theta aléatoire
x, y = make_regression(n_samples=2, n_features=1, noise=10)
plt.scatter(x, y, label="Data") # afficher les résultats. X en abscisse et y en ordonnée

#print("La taille de x est ",x.shape)
y=y.reshape(y.shape[0],1) #Permet de rajouter le 1 au dimension du vecteur y
#print("La taille de y est ",y.shape)

# Matrice X

X= np.hstack((x, np.ones(x.shape)))
print("La forme de la Matrie X est ",X.shape)
print("La Matrice X vaut ",X)

np.random.seed(0) # pour produire toujours le meme vecteur theta aléatoire
theta=np.random.randn(2,1)
print("La forme de la theta est ",theta.shape)
print("theta vaut ",theta)

print("Le Model vaut ",Model(X, theta))

plt.plot(x,Model(X,theta),c='r',label="Droite d'initialisation")
plt.title("Graphique à l'inialisation" )
plt.xlabel("Axe des X")
plt.ylabel("Axe des Y")
plt.legend()


a=cost_function(X, y, theta)
print("La fonction coût vaut = ",a)

#Machine Learning

theta_final, cost_history =gradient_descent(X, y, theta, learning_rate=0.01, nb_iteration=1000)
print("theta_final= ",theta_final)

prediction=Model(X, theta_final)

plt.figure()
plt.scatter(x,y, label="Data")
plt.plot(x, prediction,c='r', label="Prediction du model")
plt.title("Graphique à la fin du Machine Learning")
plt.xlabel("Axe des X")
plt.ylabel("Axe des Y")
plt.legend()

plt.figure()
plt.plot(range(1000),cost_history , label="Coût de la fonction")
plt.title("Graphique du coût")
plt.xlabel("Axe des X")
plt.ylabel("Axe des Y")
plt.legend()
plt.show()
 
a=coef_determaination(y,prediction)
print("Le coefficient de determaintion vaut ",a)
