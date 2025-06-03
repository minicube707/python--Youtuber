import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.svm import  SVR

#Faire notre  propre système de métrique

#Une métrique est une mesure ou une valeur numérique qui permet d'évaluer la performance, dans notre cas de minimiser l'erreur

np.random.seed(0)

m=100
X=np.linspace(0, 4, m).reshape(m, 1)
y= 2 + X**1.3 + np.random.randn(m, 1)
y=y.ravel()

plt.figure()
plt.scatter(X, y)
plt.title("Data")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

model=LinearRegression()
model.fit(X,y)
y_pred=model.predict(X)

plt.figure()
plt.title("Prédiction du model")
plt.scatter(X,y)
plt.plot(X, y_pred, c='r',label="Model")
plt.plot(X, y + y*0.2, c='g', ls='--',label="Borne positive")
plt.plot(X, y - y*0.2, c='g', ls='--',label="Borne négative")
plt.legend()
plt.show()

#Création de notre fonction métrique
def custom_metric(y, y_pred):
    return  np.sum((y_pred < y + y*0.2)&(y_pred > y - y*0.2))/y.size 

print("")
print("Le pourcentage d'erreur du model par notre système de métrique")
print(custom_metric(y, y_pred))

#Pour utiliser notre métrique, il faut la faire passer dans la fonction make_scorer()
#Le parmètre greater_is_better(), permet de savoir si plus notre score est élévé meilleurs sera nos performances

custom_score = make_scorer(custom_metric, greater_is_better=True)


#Une fois notre métrique passer dans la fonction make__score, on peut l'utiliser dans un cross_val_score() ou dans un model avec GridSearchCV()
#dans le paramètre scoring= dans les deux cas
res=cross_val_score(LinearRegression(), X, y, cv=3, scoring=custom_score)
print("")
print("Résultat de notre métrique par la cross_validation")
print(res)

model = SVR(kernel='rbf', degree=3)
params={'gamma':np.arange(0.1, 1, 0.05)}

grid=GridSearchCV(model, param_grid=params, cv=3, scoring=custom_score)

train_model=grid.fit(X,y)

print("")
print("Notre model entrainnné")
print(train_model)

best_model=grid.best_estimator_
y_pred=best_model.predict(X)

res=custom_metric(y, y_pred)
print("")
print("Le pourcentage de réussite de notre model entrainner par notre métrique")
print(res)

plt.figure()
plt.title("Prédiction du model avec le nouveau système de métrique")
plt.scatter(X,y)
plt.plot(X, y_pred, c='r',label="Model")
plt.plot(X, y + y*0.2, c='g', ls='--',label="Borne positive")
plt.plot(X, y - y*0.2, c='g', ls='--',label="Borne négative")
plt.show()

#Exercice

def RMSE(y, y_pred):
    return np.sqrt(1/y.size*np.sum((y-y_pred)**2))

RMSE_score=make_scorer(RMSE, greater_is_better=True)