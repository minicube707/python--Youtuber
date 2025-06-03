import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import SGDClassifier
from sklearn.impute import SimpleImputer, KNNImputer, MissingIndicator
from sklearn.pipeline import make_union, make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV

#SimpleImputer

X=np.array([[10,3],
            [3,4],
            [5,3],
            [3,4],
            [np.nan,3]])
print(X)

#missing_values=Valeurs manquant

#strategy=mean
print("")
print("#strategy=mean")

#strategy=mean: la(s) valeur(s) manquante(s) sera(iant) remplacée(s) par la moyenne des autres valeurs existantes
mean_imputer=SimpleImputer(missing_values=np.nan,strategy='mean')
X_res=mean_imputer.fit_transform(X)

print(X_res)

#strategy=medeian
print("")
print("#strategy=medeian")

#strategy=median: la(s) valeur(s) manquante(s) sera(iant) remplacée(s) par la médianne des autres valeurs existantes
median_imputer=SimpleImputer(missing_values=np.nan,strategy='median')
X_res=median_imputer.fit_transform(X)

print(X_res)

#strategy=most_frequent
print("")
print("#strategy=most_frequent")

#strategy=most_frequent: la(s) valeur(s) manquante(s) sera(iant) remplacée(s) par la valeur de la valeurs la plus fréquent. 
#Peut être utilisé avec des strings
fre_imputer=SimpleImputer(missing_values=np.nan,strategy='most_frequent')
X_res=fre_imputer.fit_transform(X)

print(X_res)

#strategy=constant
print("")
print("#strategy=constant")

#strategy=constant: la(s) valeur(s) manquante(s) sera(iant) remplacée(s) par ne valeur constant, definie par le parmètre fill_value.
#Peut être utilisé avec des strings
con_imputer=SimpleImputer(missing_values=np.nan,strategy='constant', fill_value=-1)
X_res=con_imputer.fit_transform(X)

print(X_res)

#Subtilité
print("")
print("#Subtilité")

#Quand je passe mes données dans un transfomer, afin qu'il s'entraine et format les données
X_train=np.array([[10,3],
                  [3,4],
                  [5,3],
                  [3,4],
                  [np.nan,np.nan]])

print("")
print("Train_set\n",X_train)

mean_imputer_train=SimpleImputer(missing_values=np.nan,strategy='mean')
X_res=mean_imputer_train.fit_transform(X_train)

print("")
print("Train_set formaté\n",X_res)

#Si je passe à travers d'autres  données sans l'entrainner dessus, alors les données seront formatées en fonction des données passer
X_test=np.array([[11,3],
                 [4,4],
                 [6,3],
                 [8,4],
                 [np.nan,np.nan]])

print("")
print("Test_set\n",X_test)

X_res=mean_imputer_train.transform(X_test)

print("")
print("Test_set formaté sans l'entrainner le transformateur\n",X_res)

print("")
print("Autre exemple")

X_test=np.array([[11,3],
                 [4,np.nan],
                 [np.nan,3],
                 [8,4],
                 [5,8]])

print("")
print("Autre Test_set\n",X_test)

X_res=mean_imputer_train.transform(X_test)

print("")
print("Autre Test_set formaté sans l'entrainner le transformateur\n",X_res)

#Mais si je réentrainne mon formateur
X_test=np.array([[11,3],
                 [4,4],
                 [6,3],
                 [8,4],
                 [np.nan,np.nan]])

print("")
print("Test_set\n",X_test)

X_res=mean_imputer_train.fit_transform(X_test)
print("")
print("Test set formaté et entrainant le transformer\n",X_res)

#KNNImputer
print("")
print("#KNNImputer")

X=np.array([[1,100],
            [2,30],
            [3,15],
            [np.nan,20]])

print("")
print("data\n",X)

#missing_values: pour indiquer la valeur manquante
#n_neighbors: Pour indiquer le nombres de voisin qui influront le résulatat
#weights: 'uniform' la distance ne joue aucun rôle. 'distance' les valeurs plus proche auront plus d'influance que les valeurs plus loin

imputer=KNNImputer(n_neighbors=1)
X_res=imputer.fit_transform(X)

print("")
print("res\n",X_res)

#MissingIndicator
#Renvoie un tableau de booléens qui indique s'il manque des données

X=np.array([[1,100],
            [2,30],
            [3,15],
            [np.nan,np.nan]])

print("")
print("Donnée \n",X)

res=MissingIndicator().fit_transform(X)

print("")
print("res \n",res)

#Exemple
print("")
print("#Exemple")

X=np.array([[1,100],
            [2,30],
            [3,15],
            [np.nan,np.nan]])

print("")
print("Donnée \n",X)

#Création d'un pipeline qui remplace les valeurs manquantes par -99
pipline=make_union(SimpleImputer(missing_values=np.nan,strategy='constant', fill_value=-99),MissingIndicator())
res=pipline.fit_transform(X)

print("")
print("Tableau dont les données manquantes ont était remplacé par -99\n",res)

#Démo
print("")
print("#Démo")

titanic=sns.load_dataset('titanic')
X=titanic[['pclass','age']]
y=titanic['survived']

X_train,X_test,y_train,y_tesy=train_test_split(X,y, random_state=0)

model=make_pipeline(KNNImputer(), SGDClassifier())

print("")
print("model: ", model)

params={'knnimputer__n_neighbors' : [1, 2, 3, 4]}

grid=GridSearchCV(model, param_grid=params, cv=5)

grid.fit(X_train,y_train)
res=grid.best_params_

print("")
print("Les meilleurs paramètres sont :", res)