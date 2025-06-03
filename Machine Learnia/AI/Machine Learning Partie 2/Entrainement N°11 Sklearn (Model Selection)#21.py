import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import validation_curve
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import learning_curve

iris =load_iris()

X = iris.data
y = iris.target

print("La shape de X est ",X.shape)

plt.figure()
plt.scatter(X[:,0], X[:,1], alpha=0.8, c=y)
plt.title("Data_set des fleurs d'iris")
plt.show()

#train_test_split()
#Permet de séparer ses données en deux groupes

#Le train_set: Ce sont les données qui vont entrainner le model

#Le test_set: Ces données sont cachées au model, il servent à vérifier l'apprentissage du model.
#Il évalue à quel point le modèle est capable de faire des prédictions précises sur de nouvelles données.
#L'utilisation d'un ensemble de test distinct est cruciale pour éviter le surapprentissage (overfitting),
#où le modèle s'ajuste trop bien aux données d'entraînement mais ne peut pas généraliser correctement.

#Généralement au coupe les données à 80%, donc 80% train_set et 20% test_set, d'où le test_size=0.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5) 

print("")
print("Train set: ",X_train.shape)
print("Test set: ",X_test.shape)

plt.figure(figsize=(12,4))
plt.subplot(121)
plt.title("Train set")
plt.scatter(X_train[:,0], X_train[:,1], c=y_train ,alpha=0.8)

plt.subplot(122)
plt.title("Test set")
plt.scatter(X_test[:,0], X_test[:,1], c=y_test ,alpha=0.8)
plt.show()

model = KNeighborsClassifier(n_neighbors=1)

model.fit(X_train, y_train)
print('')
print("Train Score: ",model.score(X_train, y_train))
print("Test  Score: ",model.score(X_test, y_test))

#CrossValidation

#cross_val_score()
#La validation croisée est une technique d'évaluation des performances qui consiste à diviser votre ensemble de données
#en plusieurs sous-ensembles (plis ou folds)
#Cela permet d'évaluer le modèle de manière plus robuste, car il est testé sur différentes parties des données.
#Permet de découper les données du test_set et du train_set et de les faire changer de set
#Afin de trouver les meilleurs hyperparamètres de notre model
#cv: est le paramétre qui indique le nombre de découpe du data_set

cross_score = cross_val_score(KNeighborsClassifier(), X_train, y_train, cv=5)

print("")
print("Le val_score est de :")
print(cross_score)
print("")
print("La moyenne est de ")
print(cross_score.mean())

model = KNeighborsClassifier()
k=np.arange(1,50)

#validation_curve()
#Permet de tester toutes les valeurs pour un hyperparamétre donné

#L'hyperparamètre que vous souhaitez régler est spécifié à l'aide de l'argument param_name=. Ici 'n_neighbors'.

#Vous spécifiez les différentes valeurs de l'hyperparamètre que vous souhaitez tester à l'aide de l'argument param_range=. Ici k.

#Vous spécifiez la métrique de performance que vous souhaitez utiliser pour évaluer le modèle à l'aide de l'argument scoring.
#Par exemple, si vous utilisez scoring='accuracy', cela signifie que vous évaluez la précision du modèle pour chaque valeur de l'hyperparamètre.

#cv est le nombre de découpe de notre dataset

#Val_score vaut donc (49,5), car nous avons testé 49 valeurs qui sont dans 'k' et 5 car cv=5

#Résultat: La fonction validation_curve() renvoie les scores de performance du modèle pour chaque valeur de l'hyperparamètre dans param_range.
#Ces scores peuvent être utilisés pour visualiser comment la performance du modèle varie en fonction de la valeur de l'hyperparamètre.

train_score, val_score =  validation_curve(model, X=X_train, y=y_train, param_name='n_neighbors', param_range=k, cv=5)

print("")
print("val_score. shape=",val_score.shape)
print("")
print("val_score:")
print(val_score)

print("")
moyenne_score=val_score.mean(axis=1)
print("val_score.mean():")
print(moyenne_score)

print("")
print("train_score. shape=",train_score.shape)
print("")
print("train_score:")
print(train_score)

print("")
moyenne_train=train_score.mean(axis=1)
print("train_score.mean():")
print(moyenne_train)

plt.figure()
plt.plot(k, moyenne_score, label="val_score")
plt.plot(k, moyenne_train, label="train_score")
plt.xlabel('n_neighbors')
plt.ylabel('score')
plt.legend()
plt.show()

#GridSearchCV
#GridSearchCV est un outil puissant pour l'optimisation des hyperparamètres d'un modèle d'apprentissage automatique.
#Il s'agit d'une technique de recherche systématique des meilleures combinaisons d'hyperparamètres pour un modèle donné.
#Ainsi GridSearchCV créer une grille de modèle avec toutes les  combinaisons d'hyperparamètres présent dans param_grid

print("")
print("#GridSearchCV")
print("")

#param_grid est un dico contenant en tant que les clés nos hyperparamétres à tester et les valeurs à tester danss les valeurs du dico
param_grid = {'n_neighbors':np.arange(1,20), 'metric': ['euclidean', 'manhattan']}

grid = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5)

grid.fit(X_train, y_train)

print("Le meilleur score est ", grid.best_score_)
print("Les meilleurs scores sont ", grid.best_params_)

model=grid.best_estimator_
res=model.score(X_test,y_test)
print(res)

#Leaning Curve
print("")
print("#Leaning Curve")
print("")

#learning_curve()
#learning_curve() permet de voir la progréssion du model en fonction de la taille du data_set
#Le paramétre train_sizes= permet de savoir comment découper le data_set

#Visualisation : Vous pouvez utiliser les résultats de learning_curve() pour visualiser comment la performance du modèle évolue
#à mesure que la taille de l'ensemble d'entraînement augmente.
#Cela peut vous donner des informations importantes sur l'efficacité de votre modèle et vous aider à déterminer 
#si davantage de données d'entraînement sont nécessaires ou si le modèle atteint un plateau de performance.

#Résultat:La fonction learning_curve() retourne 3 variables
#train_size est un tableau contenant les indices de la découpe de notre data_set
#La fonction learning_curve() renvoie les scores de performance du modèle pour chaque découpge de notre data_set.
#Ces scores peuvent être utilisés pour visualiser comment la performance du modèle varie en fonction de la taille du data_set.

train_size, train_score, val_score = learning_curve(model, X_train, y_train, train_sizes=np.linspace(0.1, 1.0, 10), cv=5)

print("train_size=\n",train_size)
print("")
print("train_score=\n",train_score)
print("")
print("val_score=\n",val_score)
print("")

plt.figure()
plt.plot(train_size,train_score.mean(axis=1), label="train")
plt.plot(train_size,val_score.mean(axis=1), label="validation")
plt.xlabel("Taille du train_set")
plt.ylabel("Taux de réussite du model")
plt.legend()
plt.show()


#Exercice
print("")
print("#Exercice")
print("")

titanic = sns.load_dataset('titanic')
print('')
print(titanic.head())

titanic = titanic[['survived','pclass','sex','age']]
titanic.dropna(axis=0, inplace=True)
titanic['sex'].replace(['male', 'female'],[0,1], inplace=True)

print('')
print(titanic.head())

model = KNeighborsClassifier()

y=titanic['survived']
X=titanic.drop('survived', axis=1)

print('')
print('y=')
print(y)

print('')
print('X=')
print(X)

X_train_titanic, X_test_titanic, y_train_titanic, y_test_titanic = train_test_split(X, y, test_size=0.2, random_state=5) 

param_grid = {'n_neighbors':np.arange(1,20)}

grid = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5)

grid.fit(X_train_titanic, y_train_titanic)

print("Le meilleur score est ", grid.best_score_)
print("Les meilleurs scores sont ", grid.best_params_)

model=grid.best_estimator_
res=model.score(X_test_titanic,y_test_titanic)
print(res)