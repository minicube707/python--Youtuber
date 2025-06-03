import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsClassifier

#Regression Linéaire avec SKLearn

print("#Regression Linéaire avec SKLearn")

np.random.seed(0)
m = 100 #Sample
X = np.linspace(0,10,m).reshape(m,1)
y = X + np.random.randn(m,1)

plt.figure()
plt.scatter(X,y)
plt.title("Model Linéaire")
plt.show()

model=LinearRegression()

#Le model s'entrainne sur les données
model.fit(X,y)

#Le model est fiable à tant de pourcent
model.score(X,y)
print('')
print("Les prédictions du model sont correctes à ")
print(model.score(X,y))

#Le model est utilisable avec de nouvelle données
model.predict(X)
print('')
print("Les prédictions sont")
print(model.predict(X))

prediction=model.predict(X)

plt.figure()
plt.scatter(X,y)
plt.plot(X,prediction, c='r')
plt.title("Prediction du model")
plt.show()

#Model Linéaire sur Data  Polynomial

np.random.seed(0)
m = 100 #Sample
X = np.linspace(0,10,m).reshape(m,1)
y = X**2 + np.random.randn(m,1)

plt.figure()
plt.scatter(X,y)
plt.title("Model Non-Linéaire")
plt.show()

model=LinearRegression()

model.fit(X,y)

model.score(X,y)
print('')
print("Les prédictions du model sont correctes à ")
print(model.score(X,y))

model.predict(X)
print('')
print("Les prédictions sont")
print(model.predict(X))

prediction=model.predict(X)

plt.figure()
plt.scatter(X,y)
plt.plot(X,prediction, c='r')
plt.title("Prediction incorrecte du model")
plt.show()

#Regression Non-Linéaire avec SKLearn

print("")
print("#Regression Non-Linéaire avec SKLearn")

np.random.seed(0)
m = 100 #Sample
X = np.linspace(0,10,m).reshape(m,1)
y = X**2 + np.random.randn(m,1)

plt.figure()
plt.scatter(X,y)
plt.title("Model Non Linéaire")
plt.show()

model=SVR(C=100)

model.fit(X,y)

model.score(X,y)
print('')
print("Les prédictions du model sont correctes à ")
print(model.score(X,y))

model.predict(X)
print('')
print("Les prédictions sont")
print(model.predict(X))

prediction=model.predict(X)

plt.figure()
plt.scatter(X,y)
plt.plot(X,prediction, c='r')
plt.title("Prediction du model")
plt.show()

#Classifiaction
print("")
print("#Classifiaction")

titanic = sns.load_dataset('titanic')
print('')
print(titanic.head())

titanic = titanic[['survived','pclass','sex','age']]
titanic.dropna(axis=0, inplace=True)
titanic['sex'].replace(['male', 'female'],[0,1], inplace=True)

print('')
print(titanic.head())

model_survie = KNeighborsClassifier(n_neighbors=4)

y_titanic=titanic['survived']
X_titanic=titanic.drop('survived', axis=1)

print('')
print('y_titanic=')
print(y_titanic)

print('')
print('X_titanic=')
print(X_titanic)

model_survie.fit(X_titanic,y_titanic)

print('')
print("Les prédictions du model sont correctes à ")
print(model_survie.score(X_titanic,y_titanic))

print('')
print("Les prédictions sont")
print(model_survie.predict(X_titanic))

def survie( model_survie, pclass=3,  sex=0 ,age=19):
    
    X=np.array([pclass, sex, age]).reshape(1,3)

    print("")
    print("Voici X")
    print(X)

    print("")
    print("Les prediction sont")
    a=model_survie.predict(X)
    print(a)

    if a==0:
        print("Je suis mort")
    else:
        print("Je suis vivant")

    print("")
    print("Les proba sont")
    print(model_survie.predict_proba(X))

survie(model_survie)

