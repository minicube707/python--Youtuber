
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
        theta=theta-learning_rate*grad(X, y, theta)
        cost_history[i]=cost_function(X,y,theta)

    return theta, cost_history

def coef_determaination(y,prediction):
    u=((y-prediction)**2).sum()
    v=((y-y.mean())**2).sum()
    return 1-u/v

#Main
np.random.seed(0)
x = np.linspace(-2, 3, 40)  
x = x.reshape((x.size, -1))

y = x**3 -2*x**2 - 3*x +1 + (np.random.rand(40,1)-0.5)
plt.figure()
plt.scatter(x, y, label="Data") # afficher les résultats. X en abscisse et y en ordonnée

y=y.reshape(y.shape[0],1) 

#Matrice X
X = np.ones(x.shape)
X = np.hstack((np.sin(x),X))
X = np.hstack((np.cos(x),X))
X = np.hstack((np.sin(2*x),X))
X = np.hstack((np.cos(2*x),X))
theta=np.random.rand(5,1)

plt.plot(x,Model(X,theta),c='r',label="Droite d'initialisation")
plt.title("Graphique à l'inialisation" )
plt.xlabel("Axe des X")
plt.ylabel("Axe des Y")
plt.legend()

fcoup_initial=cost_function(X, y, theta)

#Machine Learning

theta_final, cost_history =gradient_descent(X, y, theta, learning_rate=0.01, nb_iteration=1000)

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
 
cdet=coef_determaination(y,prediction)
fcoup_final=cost_function(X, y, theta)

print("")
print("La fonction coût initial vaut = ",fcoup_initial)
print("La fonction coût final vaut = ",cost_history[-1])
print("theta_initial vaut ",theta[0]," et ",theta[1])
print("theta_final vaut ",theta_final[0]," et ",theta_final[1])
print("Le coefficient de determaintion vaut ",cdet)
print("")
