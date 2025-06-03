import numpy as np
import matplotlib.pyplot as plt 
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import StandardScaler,OneHotEncoder, Binarizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.impute import SimpleImputer
import seaborn as sns


titanic= sns.load_dataset('titanic')
print(titanic.head())

#Sur notre dataset on'a des valeurs numériques et des lettres
#Or StandardScaler() ne peut pas utiliser les lettres
#Pour palier à ce problème, on utilise  make_column_transformer(), qui permet de selectioner uniquement les colonnes choisi

y=titanic['survived']
X=titanic.drop(["survived"], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

#J'applique grâce à make_column_transformer(), le tramsfomer StandardScaler() sur les colonnes 'age','fare'
transfromer=make_column_transformer((StandardScaler(),['age','fare']))
res=transfromer.fit_transform(X)

print("")
print("Voici les données de mes colonnes age','fare' transfomé par StandardScaler()")
print(res)

#Pour transformer notre tableau, nous allons découper notre tableau en deux catégorie, une numérique, et une catégorique

numerical_features=['pclass','age','fare']
categorical_features=['sex','deck','alone']

numerical_pipeline = make_pipeline(SimpleImputer(strategy='mean'), StandardScaler())
categorical_pipeline = make_pipeline(SimpleImputer(strategy='most_frequent'), OneHotEncoder())

#Grâce à make_column_transformer(), je normalise mes données numérique et corrige les données manquant
#et je je transforme mes données caractéristique en données numérique et corrige les données manquant
preprocessor = make_column_transformer((numerical_pipeline, numerical_features),(categorical_pipeline, categorical_features))

  
model=make_pipeline(preprocessor,SGDClassifier())
res=model.fit(X_train, y_train)
print("")
print("Model:")
print(res)

#Mais si on veut traiter toutes nos données alors on peut utiliser  make_column_selector()
#Alors on a: 

print("")
print("make_column_selector()")

#Ici grâce à make_column_selector(), on répartie les colonnes avec numbre (dtype_include = np.number) et les colonnes avec des lettres (dtype_exclude=np.number)
numerical_features=make_column_selector(dtype_include = np.number)
categorical_features=make_column_selector(dtype_exclude=np.number)

print("")
print("numerical_features ('adresse mémoire de l'objet en mémoire):",numerical_features,"\n")
print("categorical_features ('adresse mémoire de l'objet en mémoire):",categorical_features,"\n")


#Ici, on a créer un objet pipline, dans lequel, on a deux transformer

#SimpleImputer() est un transformateur de données utilisé pour remplacer 
#les valeurs manquantes dans un ensemble de données par des valeurs définies

#strategy='mean' cela veut dire que les données manquantes seront remplacées par la moyenne des valeurs existantes
#strategy='most_frequent' cela veut dire que les données seront remplacées par la valeur la plus fréquentes

#StandardScaler() est un transformateur de données qui effectue la mise à l'échelle standard des caractéristiques numériques.
#OneHotEncoder() est un tramsfomer de données qui effectue la transformation de carractère en nombre

numerical_pipeline = make_pipeline(SimpleImputer(strategy='mean'), StandardScaler())
categorical_pipeline = make_pipeline(SimpleImputer(strategy='most_frequent'), OneHotEncoder())

#Ansi arriver ici, je modifie tout mon tableau
preprocessor = make_column_transformer((numerical_pipeline, numerical_features),(categorical_pipeline, categorical_features))

model=make_pipeline(preprocessor,SGDClassifier())
res=model.fit(X_train,y_train)

print("")
print("Model:")
print(res)

res=model.score(X_test, y_test)

print("")
print("Score du model:",res)

numerical_features=X[['age','fare']]

#Comme la colonne age contient des 'nan', il faut les transformer pour que le transfomer Binarizer() puissent les exploiter
#Création d'un pipeline, contenant, le type de valeurs manquant, et la stratégie à adoptée
pipline_SimpImputer=SimpleImputer(missing_values=np.nan,strategy='most_frequent')

#Application du pipeline pour retirer les valeurs manqauntes
numerical_features_without_nan=pipline_SimpImputer.fit_transform(numerical_features)

#Make_union(), permet de mettre en parallèle plusieurs transformer()
pipline_two_transfomer=make_union(StandardScaler(), Binarizer())

#On obteint 4 colonnes : age+StandardScaler(), age+Binarizer(), fare+StandardScaler(),fare+Binarizer()
res=pipline_two_transfomer.fit_transform(numerical_features_without_nan)

print("")
print("On obteint 4 colonnes : age+StandardScaler(), age+Binarizer(), fare+StandardScaler(),fare+Binarizer()")
print("La shape est de ",res.shape,"\n")
print(res)