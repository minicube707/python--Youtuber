import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import os


#Execution du fichier
current_directory = os.getcwd()
print("Répertoire de travail actuel :", current_directory)

# Déplacer l'exécution vers un autre répertoire
new_directory = "Desktop\Document\Programme\Python\AI\Data"
os.chdir(new_directory)

#Execution du fichier
current_directory = os.getcwd()
print("Répertoire de travail actuel :", current_directory)


# Charger le fichier Excel depuis le nouveau répertoire
data_main = pd.read_excel("titanic.xls")

print('')
print(data_main)
print('')
print("Les dimensions du ficheir exel sont ")
print(data_main.shape)
print('')
print("Les différentes colonnes sont :")
print(data_main.columns)
print('')
print("Les premières lignes sont :")
print(data_main.head())

#Purification des données

#.drop() Permet de retirer les colonnes ou ligne d'un tableau
data=data_main.drop(['name','sibsp','parch','ticket','fare','cabin','embarked','boat','home.dest','body'],axis=1)
data_frame=data_main.drop(['sibsp','parch','ticket','fare','cabin','embarked','boat','home.dest','body'],axis=1)

print('')
print("Le dataset simplifié ")
print(data)

print('')
print("Les nouvelles dimensions du ficheir exel sont ")
print(data.shape)

print('')
print("Les nouvellles colonnes sont :")
print(data.columns)

print('')
print("Les premières lignes du dataset simplifié :")
print(data.head())

print('')
print("Voici un premier jet de statistique ")
print(data.describe())

#Des données ont été corompu 
#Permet de retirer les données manquantes
data=data.dropna(axis=0)

print('')
print("Les nouvelles dimensions du ficheir exel après avoir retirer les données manquant sont ")
print(data.shape)
print('')
print("Le dataset simplifié ")
print(data)
print('')
print("Voici un premier jet de statistique ")
print(data.describe())

#Value_counts()
print('')
print("Voici les nombres de personnes dans les différentees classes")
print(data['pclass'].value_counts())

plt.figure()
data['pclass'].value_counts().plot.bar()
plt.title("Histogramme représentant la proportion des classes du titanic")
plt.show()

print('')
print("Voici les nombres des différents ages")
print(data['age'].value_counts())

plt.figure()
data['age'].hist()
plt.title("Histogramme représentant la proportion des ages du titanic")
plt.show()

print('')
print("Voici les nombres des sexes")
print(data['sex'].value_counts())

plt.figure()
data['sex'].value_counts().plot.bar()
plt.title("Histogramme représentant la proportion des sexes du titanic")
plt.show()

#groupby()
print("\n")
print('Voici les data sur le sexe')
print("")
print(data.groupby(['sex']).mean())

print("\n")
print('Voici les data sur le sexe et la classe')
print("")
#Permet de faire des statistiques sur les groupes
print(data.groupby(['sex','pclass']).mean())

#DataFrame et Séries

print("")
print("Voici la séries sur l'age")
print(data['age'])

#set_index("") Permet de créer son propre index
data_frame=data_frame.set_index('name')
print("")
print("Voici la séries sur l'age indexer sur le nom")
print(data_frame['age'])

#Indexing
print("")
print("Voici les dix première colonnes sur l'age du dataset")
#A gauche on a une série:data['age']      
# A droite c'st l'indexing:[0:10]
print(data['age'][0:10])

print("")
print("Voici le masque des pasagers mineurs")
print(data['age']<18)

print("")
print("Répartions des mineurs sur les différentes classes")
print(data[data['age']<18]['pclass'].value_counts())

print("")
print("Répartions des mineurs sur les différentes classes et leurs sexes")
print(data[data['age']<18].groupby(['sex','pclass']).mean())

#Loc Permet d'accédez à un groupe de lignes et de colonnes par étiquette ou par un tableau booléen.
#Iloc Indexation purement basée sur l’emplacement entier pour la sélection par position.

# Permet d'utiliser le tableau avec des indices
print("")
print("Affichage des 5 première lignes et 3 première colonnes")
print(data_main.iloc[0:5,0:3,])

print("")
print("Affichage des 3 première lignes de la colonnes age")
print(data_main.loc[0:2,['age']])

print("")
print("Affichage des 3 première lignes de la colonnes age et classe")
print(data_main.loc[0:2,['age','pclass']])

#Exercice

data.loc[data['age']<=20,'age']=0
data.loc[(data['age']>20)&(data['age']<=30),'age']=1
data.loc[(data['age']>30)&(data['age']<=40),'age']=2
data.loc[data['age']>40]=3

print("")
print("Exercie")
print(data)

def category_age(ages):
    if ages<=20:
        return '<20 ans'
    elif (ages>20) & (ages<=30):
        return '20-30 ans'
    elif (ages>30) & (ages<=40):
        return '30-40 ans'
    else:
        return '+40 ans'

#map() Permet de remplace les valeurs d'une colonne à partir d'un fonction ou d'une défintion 
#apply() C'est pareil que map(), mais appliqué sur tout le dataframe
print("")
print("Tableau découpé selon la tranche d'age")
print(data_main['age'].map(category_age))

print("")
print("Tableau découpé selon lze sex. Avec male=0 et female=1")
print(data_main['sex'].map({'male':0,'female':1}))

#replace() Permet de remplacer un caractére par un autre
print("")
print(data_main['sex'].replace(['male','female'],[0,1]))

#Permet de compter le nombre de fois qu'une catégorie apparrait
print("")
print(data_main['sex'].astype('category'))

#Grace à .cat.codes on transforme les catégories en valeurs numérique
print("")
print(data_main['sex'].astype('category').cat.codes)