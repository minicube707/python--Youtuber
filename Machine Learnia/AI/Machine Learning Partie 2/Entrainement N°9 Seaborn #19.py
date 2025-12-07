import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)
os.chdir("../Data")

flower = pd.read_csv("iris.csv")
print('')
print(flower.head())

plt.figure()
plt.scatter(flower['sepal_length'], flower['sepal_width'])
plt.title("Graphique sur la relation entre\n la longueur du sépal et la largeur du sépal")
plt.show()

iris = sns.load_dataset('iris')
print('')
print(iris.head())

#Créer une page avec les relations entre touts les graphiques
sns.pairplot(iris)
plt.show()

#Créer une page avec les relation entre tout les graphiques avec des couleurs pour différenciers les différentes espèces
sns.pairplot(iris, hue='species')
plt.show()

titanic = sns.load_dataset('titanic')
titanic.drop(['alone', 'alive', 'who', 'adult_male', 'embark_town', 'class'], axis=1, inplace=True)
titanic.dropna(axis=0, inplace=True)
print('')
print(titanic.head())


#data="d'ou vient les données"
#hue="séparer par quelle condition"
sns.catplot(x='survived', y='age', data=titanic, hue='sex')
plt.title("Distrubution des passagers selon leurs sex, leurs ages et\n si ils ont survécus")
plt.show()

sns.catplot(x='survived', y='age', data=titanic, hue='pclass')
plt.title("Distrubution des passagers selon leurs classes, leurs ages et\n si ils ont survécus")
plt.show()

sns.pairplot(titanic)
plt.show()

sns.displot(titanic['fare'], kind='hist')
plt.title("kind='hist'")

sns.displot(titanic['fare'], kind='kde')
plt.title("kind='kde'")

sns.displot(titanic['fare'], kind='ecdf')
plt.title("kind='ecdf'")

sns.displot(titanic['fare'], kde=True)
plt.title("kde=True")

sns.displot(titanic['fare'], aspect=2)
plt.title("aspect=2")

sns.displot(titanic['fare'], height=7)
plt.title("height=7")

plt.show()

sns.jointplot(x='age', y='fare', data=titanic, kind='hex')
plt.show()

sns.heatmap(titanic.corr())
plt.show()
