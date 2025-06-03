import numpy as np
from sklearn.preprocessing import LabelEncoder,OrdinalEncoder,OneHotEncoder,LabelBinarizer,MinMaxScaler,StandardScaler,RobustScaler
from sklearn.preprocessing import PolynomialFeatures,Binarizer, KBinsDiscretizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression, SGDClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

#Transfomer
print("")
print("#Transfomer")
print("")
print("#LabelEncoder")
print("Le transfomer LabelEncoder() est conçu pour les labels y, données de 1 dimension ")

#Méthode 1: La méthode fit() est utilisée pour estimer les paramètres d'un transformateur ou 
#d'un modèle à partir des données d'entraînement.
#Elle calcule ces paramètres en fonction des données fournies, mais ne transforme pas réellement les données.
#En d'autres termes, fit() "apprend" à partir des données d'entraînement sans modifier ces données.

#Méthode 2: La méthode transform() est utilisée pour appliquer les transformations calculées précédemment à de nouvelles données,
#en utilisant les paramètres appris avec fit().
#Cette méthode prend les données d'entrée et les transforme selon les paramètres estimés pendant l'étape fit().
#Elle est utilisée uniquement pour les données (ou les échantillons) après l'apprentissage initial.

#Méthode 3:a méthode fit_transform() combine les étapes fit() et transform() en une seule étape.
#Elle est utilisée pour estimer les paramètres à partir des données d'entraînement et transformer ces données en une seule opération.
#fit_transform() est souvent utilisée pour économiser du temps de calcul,
#car elle évite de parcourir les données deux fois (une fois pour fit() et une fois pour transform()).

#Méthode 1
print("")
print("#Méthode 1")
y=np.array(['Chat', 'Chien', 'Chat', 'Oiseau'])

transformer= LabelEncoder()
resultat=transformer.fit(y)
print(resultat)

#Methode 2
print("")
print("#Méthode 2")
resultat=transformer.transform(y)
print(resultat)

#Methode 3
print("")
print("#Méthode 3")
resultat=transformer.fit_transform(y)
print(resultat)

#inverse_transform
#Pour inversé le procésus on utilise: inverse_transfor()
print("\nPour inversé le procésus on utilise: inverse_transfor()")
resultat=transformer.inverse_transform(resultat)
print(resultat)

#En combinat un transformateur et un estimteur en obtient un pipline 

#Ordinal Encoder
print("")
print("#Ordinal Encoder()")
print("Le transfomer Ordinal Encoder() est conçu pour les features X, données de plusieurs dimensions ")

X=np.array([["Chat","poil"],
            ["Chien","Poil"],
            ["Chat","poil"],
            ["Oiseau","Plume"]])

print("")
transformer=OrdinalEncoder()
resultat=transformer.fit(X)
print(resultat)
resultat=transformer.transform(X)
print(resultat)

#L'inconveiniant de cette technique cela revindrai à dire que il y aura une ordre ordianal 1<2<3
#Pour palier à ce problème on utilise 

#LabelBinarizer
print("")
print("#LabelBinarizer)")
print("Le transfomer LabelBinarizer() est conçu pour les features X, données de plusieurs dimensions ")

y=np.array(['Chat', 'Chien', 'Chat', 'Oiseau'])

print("")
transformer=LabelBinarizer()
resultat=transformer.fit(y)
print(resultat)
resultat=transformer.transform(y)
print(resultat)

#Et pour les features

#OneHotEncoder
print("")
print("#OneHotEncoder()")
print("Le transfomer OneHotEncoder() est conçu pour les features X, données de plusieurs dimensions ")

X=np.array([["Chat","poil"],
            ["Chien","Poil"],
            ["Chat","poil"],
            ["Oiseau","Plume"]])

print("")
transformer=OneHotEncoder()
resultat=transformer.fit_transform(X)
print(resultat)

#La Normalisation
print("")
print("#Normalisation")

#MinMaxScaler()
print("")
print("#MinMaxScaler()")
X=np.array([[80],
            [70],
            [120]])

print("")
scaler=MinMaxScaler()
resultat=scaler.fit_transform(X)
print(resultat)

print("")
print("Ajout de nouvelle valeur")

X_test=np.array([[90]])
res=scaler.transform(X_test)
print(res)

iris = load_iris()
X=iris.data

#Normalisation
print("")
print("#Normalisation")

scaler=MinMaxScaler()
X_Nor=scaler.fit_transform(X)
X_Sta=StandardScaler().fit_transform(X)

plt.figure()
plt.scatter(X[:,2],X[:,3],alpha=0.3,label="Données Non Normalisées")
plt.scatter(X_Nor[:,2],X_Nor[:,3],c='orange',alpha=0.3, label="Données Normalisées par MinMax")
plt.scatter(X_Sta[:,2],X_Sta[:,3],c='green',alpha=0.3, label="Données Normalisées par Stand")
plt.legend()
plt.show()

#On peut utiliser inverse_transform() pour que nos données retruve leurs taille originals
#Pour finir ce type de transformer  est sensible au Outliers, cad des données qui sont très étendue pour contrer à ça on utilise

X_Ros=RobustScaler().fit_transform(X)

plt.figure()
plt.scatter(X[:,2],X[:,3],alpha=0.3,label="Données Non Normalisées")
plt.scatter(X_Ros[:,2],X_Ros[:,3],c='orange',alpha=0.3, label="Données Normalisées par Robust")
plt.legend()
plt.show()

#PolynomialFeatures
print("")
print("#PolynomialFeatures")
print("")

#Démo
X=np.array([[1],
            [2],
            [0.5]])

calculator=PolynomialFeatures(3).fit(X)
print(calculator)
resultat=calculator.transform(X)
print(resultat)

#Sans PolynomailFeatures
X=np.linspace(0,4,100).reshape((100,1))
y=X**2+5*np.cos(X)+np.random.randn(100,1)

plt.figure()
plt.title("Sans PolynomailFeatures")
plt.scatter(X,y)
model=LinearRegression().fit(X,y)
y_pred=model.predict(X)
plt.plot(X,y_pred, c='r')
plt.show()

#Avec PolynomailFeatures
X=np.linspace(0,4,100).reshape((100,1))
y=X**2+5*np.cos(X)+np.random.randn(100,1)

#Ici le degrès de PolynomialFeatures() est de 2,
# onc vous allez générer des caractéristiques jusqu'au carré des caractéristiques originales. 

#Création de X_poly est la nouvelle matrice des caractéristiques après la transformation.
#Elle contient à la fois les caractéristiques originales et les caractéristiques polynomiales générées.
#Si X contient [a], X_poly sera une nouvelle matrice avec les caractéristiques [1, a, a^2], donc une shape de (X.size,3).
#Mais si X contient [a, b, c], alors X_poly sera une nouvelle matrice avec les caractéristiques [1, a, a^2, b, b^2, c, c^2].

#La transformation peut être utile lorsque vous entraînez des modèles d'apprentissage automatique qui ne peuvent pas capturer
#de manière linéaire les relations entre les caractéristiques et la cible.
#L'ajout de caractéristiques polynomiales peut permettre au modèle de mieux s'adapter aux données.

X_poly=PolynomialFeatures(2).fit_transform(X)
model=LinearRegression().fit(X_poly,y)
y_pred=model.predict(X_poly)

print("")
print(" X.shape=",X.shape)

print("")
print(" X_poly=",X_poly.shape)

plt.figure()
plt.scatter(X,y)
plt.title("Avec PolynomailFeatures")
plt.plot(X,y_pred, c='r')
plt.show()

#Discrétisation
print("")
print("#Discrétisation")
print("")

#Exemple
X = np.linspace(0, 5, 10).reshape((10, 1))
resultat=np.hstack((X, Binarizer(threshold=3).fit_transform(X)))
print("Donnée  binarisé")
print(resultat)

#Démo1
n_elements=40
X = np.linspace(-5, 5, n_elements).reshape((n_elements, 1))
y=(np.tanh(X)+1)/2

#theshold: c'est la valeur X qui fait basculer la valeur y de 0 à 1
y_Disc= Binarizer(threshold=0).fit_transform(X)        

plt.figure()
plt.plot(X,y)
plt.plot(X,y_Disc,c='r', ls='--')
plt.title("Exemple 1")
plt.show()

#Démo2
n_elements=40
X = np.linspace(-5, 5, n_elements).reshape((n_elements, 1))
y=np.tanh(X)

#theshold: c'est la valeur X qui fait basculer la valeur y de 0 à 1
y_Disc= Binarizer(threshold=0).fit_transform(X)*2-1        

plt.figure()
plt.plot(X,y)
plt.plot(X,y_Disc,c='r', ls='--')
plt.title("Exemple 2")
plt.show()

print("")
print("#KBinsDiscretizer")
print("")

#KBinsDiscretizer
#Vous créez une instance de la classe KBinsDiscretizer.
#Cette classe est utilisée pour discrétiser (c'est-à-dire diviser en intervalles discrets)
#des caractéristiques numériques en fonction du nombre de bacs (n_bins) spécifié.
#Dans cet exemple, n_bins est fixé à 6, ce qui signifie que chaque caractéristique numérique sera divisée en 6 intervalles distincts.

#.toarray(): La méthode .fit_transform() retourne les données discrétisées sous forme de tableau de type scipy.sparse.csr_matrix,
#qui est une structure de données optimisée pour stocker des données creuses.
#Cependant, en utilisant .toarray(), vous convertissez ces données dans un tableau NumPy standard,
#ce qui peut être plus pratique à manipuler.

X = np.linspace(0, 5, 10).reshape((10, 1))
resultat=KBinsDiscretizer(n_bins=6).fit_transform(X).toarray()
print(resultat)


#Pipline
#Combinaison d'un transfomer et d'un estimateur
print("")
print("#Pipline")
print("")

X=iris.data
y=iris.target

print("\nX.shape=",X.shape)
print("\ny.shape=",y.shape)


X_train, X_test, y_train, y_test=train_test_split(X,y)

model_with_prepro= make_pipeline(StandardScaler(),SGDClassifier(random_state=0))

model_with_prepro.fit(X_train,y_train)
res=model_with_prepro.score(X_test,y_test)
print("Score avec preporcecing ",res)

model_without_prepro=SGDClassifier(random_state=0)
model_without_prepro.fit(X_train,y_train)
res=model_without_prepro.score(X_test,y_test)
print("Score sans preporcecing ",res)


#GridSearchCV
print("")
print("#GridSearchCV")
print("")

model=make_pipeline(PolynomialFeatures(),StandardScaler(),SGDClassifier(random_state=0))
print(model)

params = {
    'polynomialfeatures__degree':[2, 3, 4],
    'sgdclassifier__penalty':['l1', 'l2']
}

grid = GridSearchCV(model, param_grid=params, cv=4)

res=grid.fit(X_train, y_train)
best_param=grid.best_params_
best_model=grid.best_estimator_

print()
print("Meilleurs params",best_param)
print("")
print(res)

best_model=grid.best_estimator_
y_pred_best=best_model.predict(X_test)

plt.figure()
plt.scatter(X_train[:,2], y_train, c='g', label="Data")
plt.scatter(X_test[:,2],y_pred_best,c='r',label="Model",alpha=0.5)
plt.legend()
plt.show()