from sklearn.feature_selection import VarianceThreshold, chi2, SelectKBest, SelectFromModel, RFECV
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import numpy as np

def trait_graph():
    longeur=150

    for hauteur in range(0,9):
        c1=np.arange(0,longeur,1)
        c2=np.full(longeur,hauteur)
        plt.plot(c1,c2,c='r',alpha=0.3)

def head_list(list):
    for i in range(10):
        print(list[i])


iris=load_iris()
X=iris.data
y=iris.target


#VarianceThreshold
print("#VarianceThreshold")


plt.figure()
plt.plot(X)
trait_graph()
plt.title("X avec les varaibles peu sensibles")
plt.legend(iris.feature_names)
plt.show()

variance_X=X.var(axis=0)

print("")
print("Variance de X ",variance_X)

#Nous indiquons grâce à threshold=0.2 que nous voudrions retirer toutes features ayant une variance <0.2
selector=VarianceThreshold(threshold=0.2)
X_trans=selector.fit_transform(X)

#Nous avons la variance de la variable sépal width qui est inférieur à 0,2
#Elle a donc était supprimer du dataset

plt.figure()
plt.plot(X_trans)
trait_graph()
plt.title("X sans les varaibles peu sensibles")
plt.legend(iris.feature_names)
plt.show()

#get_support()
#La méthode get_support() retourne un tableau booléan des variables selectionner
print("")
print("#get_support()")

get_res=selector.get_support()
print("")
print("get_res: ", get_res)

#Avec cette méthode on peut faire du booléan indexing 
features=iris.feature_names

print("")
print("iris features: ",features)

list_features=np.array(features)
indexing_list=list_features[get_res]

#Ainsi la variable pétal width n'a pas était selectionée
print("")
print("features sélectionnées: ",indexing_list)

#SelectKBest()
print("")
print("#SelectKBest()")

#SelectKBest() selectionne les k meilleurs varaibles X dont le score du test de dépendance avec y est le plus élevé 
#Prennons l'exemple du test de dépendance du chi2()
res=chi2(X,y)

#Le premier tuple indique la dépendance de la n'ème variable X avec y
#Le deuxième tuple indique les pvalue (pas à prendre en compte maintenant)
print("")
print("res=",res[0],"\n")
print("res=",res[1],"\n")

#Attention pour le .fit_transform(), il faut faire passer X et y car on en a bession pour le test de dépendance de chi2()
selector= SelectKBest(chi2,k=1)
res=selector.fit_transform(X,y)

#Ici le selector nous retourne un seul tableau contenant un seule colonne, car nous avons demander de garder que la meilleure varaible
print("k=1")
head_list(res)

#On peut vérifier quelle varaible a été retenue avec get_support()
res=selector.get_support()

print("")
print("res=",res)

#Si on passe k=1 à k=2 on a:
#Un seul tableau contenant un deux colonnes, car nous avons demander de garder que la deux meilleures varaibles
selector= SelectKBest(chi2,k=2)
res=selector.fit_transform(X,y)

print("")
print("k=2")
head_list(res)

res=selector.get_support()

print("")
print("res=",res)

#SelectFromModel()
#Ne fonctionne qu'avec les estimateurs qui développent une fonction paramétée, (attribut .coef_ ou .feature_importance_), ne marche pas 
#par exemple avec K-Nearest Neighbour  
print("")
print("#SelectFromModel()")

#On a bession de X et y car SGDClassifier() est un estimateur qui a bession de X et y
selector=SelectFromModel(SGDClassifier(random_state=0), threshold='mean')
res=selector.fit_transform(X,y)

#Ici on ne garde que les varaibles quui au dessus de la moyenne
print("res:")
head_list(res)
print("selector.get_support()",selector.get_support())

#.estimator_.coef_ permet de voir les corresondances de chaque élément au coeff associée à une caractéristique particulière
#On obtient un tableau avec n ligne qui correspond aux features et à m colonne qui correspond aux labels/targets

print("")
print("selector.estimator_.coef_:\n",selector.estimator_.coef_)

print("")
print("Si je fais la moyenne par targets alors on a:\n",selector.estimator_.coef_.mean(axis=0))

print("")
print("Si je fais la moyenne des moyennes alors on a:",selector.estimator_.coef_.mean(axis=0).mean())
print("Donc toutes les valeurs supérieurs à cette moyenne est gardées")
print("On obtient alors",selector.get_support())

#RFECV
print("#RFECV")
print("")

selector=RFECV(SGDClassifier(random_state=0), step=1, min_features_to_select=2, cv=5)
selector.fit_transform(X,y)

print("Le classement finale de nos variables :",selector.ranking_)
print("Le nombre de variable selectionner est :", selector.n_features_)
print("Le score de SGDCLassifier à chaque itération :",selector.cv_results_['mean_test_score'])

#Comme 0.77 <0.84 alors cette varaible est important pour le model