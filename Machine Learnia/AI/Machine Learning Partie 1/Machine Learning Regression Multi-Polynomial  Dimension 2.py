
import numpy as np
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt

# Defintion

#Model
def Model (X,theta):
    return X.dot(theta)

#Fonction coût
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

#Varaible
imprecis=True
degres=1
vecteur_theta=5

x, y = make_regression(n_samples=100, n_features=2, noise=0)
y=y**5
y=y.reshape(y.shape[0],1) 


theta=np.random.randn(3,1)

# Matrice X
X= np.hstack((x, np.ones((x.shape[0],1))))


while(imprecis==True):

    print("Degres=",degres)
    
    if(degres>1):
         X=np.hstack((x**degres,X))

    plt.figure()
    plt.scatter(x[:,0], y, label="Data") # afficher les résultats. X en abscisse et y en ordonnée
    plt.scatter(x[:,0],Model(X,theta),c='r',label="Droite d'initialisation")
    plt.title("Graphique à l'inialisation avec la première feature" )
    plt.xlabel("Axe des X")
    plt.ylabel("Axe des Y")
    plt.legend()

    plt.figure()
    plt.scatter(x[:,1], y, label="Data") # afficher les résultats. X en abscisse et y en ordonnée
    plt.scatter(x[:,1],Model(X,theta),c='r',label="Droite d'initialisation")
    plt.title("Graphique à l'inialisation avec la deuxième feature" )
    plt.xlabel("Axe des X")
    plt.ylabel("Axe des Y")
    plt.legend()

    fcoup_initial=cost_function(X, y, theta)

    #Machine Learning

    dtype=theta_final, cost_history =gradient_descent(X, y, theta, learning_rate=0.01, nb_iteration=1000)

    prediction=Model(X, theta_final)

    plt.figure()
    plt.scatter(x[:,0], y, c='b', label="Data")
    plt.scatter(x[:,0], prediction,c='r', label="Prediction du model")
    plt.title("Graphique à la fin du Machine Learning "'\n'"sur la premère feature de degrès %d" % degres)
    plt.xlabel("Axe des X")
    plt.ylabel("Axe des Y")
    plt.legend()

    plt.figure()
    plt.scatter(x[:,1], y, c='b', label="Data")
    plt.scatter(x[:,1], prediction,c='r', label="Prediction du model")
    plt.title("Graphique à la fin du Machine Learning "'\n'"sur la deuxième feature de degrès %d" % degres)
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
    print("La fonction coût final vaut =   ",cost_history[-1])
    print("theta_initial vaut ")
    print(theta)
    print("theta_final vaut ")
    print(theta_final)
    print("Le coefficient de determaintion vaut ",cdet)
    print("")

    if(cdet>0.9):
        imprecis=False
    else:
        degres+=1
        vecteur_theta+=2
        theta= np.vstack((theta, np.ones((2,1))))
        
