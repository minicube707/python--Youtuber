from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold, LeaveOneOut, ShuffleSplit, StratifiedKFold
from sklearn.datasets import load_iris

#CrossValidation
#Comment découper son train set 

iris =load_iris()
X = iris.data
y = iris.target


#KFold découpe le validation set de manière égal 
cv=KFold(5, random_state=0, shuffle=True)
resultat = cross_val_score(KNeighborsClassifier(), X, y, cv=cv)
print("KFold")
print(resultat)

#LeaveOneOut s'entraine sur toutes les cartes et valide sur une seule
cv=LeaveOneOut()
resultat = cross_val_score(KNeighborsClassifier(), X, y, cv=cv)
print("LeaveOneOut")
print(resultat)

#Mélange et découpe le validation set en petit pars aléatoire
cv=ShuffleSplit(4, test_size=0.2)
resultat = cross_val_score(KNeighborsClassifier(), X, y, cv=cv)
print("ShuffleSplit")
print(resultat)

# StratifiedKFold découpe chaque classe en pars égal pour le validation set
cv=StratifiedKFold(4)
resultat = cross_val_score(KNeighborsClassifier(), X, y, cv=cv)
print("StratifiedKFold")
print(resultat)