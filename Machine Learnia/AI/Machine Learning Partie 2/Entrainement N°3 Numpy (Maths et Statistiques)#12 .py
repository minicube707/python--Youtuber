import numpy as np
from datetime  import datetime

heure_actuelle = datetime.now().strftime("%H:%M:%S")
print("")
print("L'heure actuelle est :", heure_actuelle)
print("")

A=np.array([[1,2,3],
            [4,5,6],
            [7,8,9]])

print("A=")
print(A)

#Somme
print("")
print("Somme")

print("Pour faire la somme de A, on utilise A.sum() :",A.sum())
print("Pour faire la somme cumulé de A, on utilise A.cumsum() :",A.cumsum())

print("")
print("Pour faire la somme vertical de A, on utilise A.sum(axis=0) :",A.sum(axis=0))
print("Pour faire la somme horizontal de A, on utilise A.sum(axis=1) :",A.sum(axis=1))

#Produit
print("")
print("Produit")

print("Pour faire le produit du tabelau de A, on utilise A.prod() :",A.prod())
print("Pour faire le produit cumulé du tabelau de A, on utilise A.cumprod() :",A.cumprod())

print("")
print("Pour faire le produit vertical de A, on utilise A.prod(axis=0) :",A.prod(axis=0))
print("Pour faire le produit horizontal de A, on utilise A.prod(axis=1) :",A.prod(axis=1))

#Min Max
print("")
print("Max Min")

print("Pour faire le minimun de A, on utilise A.min() :",A.min())
print("Pour faire le maximun de A, on utilise A.max() :",A.max())
print("Pour faire les minimuns vericals de A, on utilise A.min(axis=0) :",A.min(axis=0))
print("Pour faire les maximuns vericals de A, on utilise A.max(axis=0) :",A.max(axis=0))
print("Pour faire les minimuns horizontals de, on utilise A.min(axis=1) :",A.min(axis=1))
print("Pour faire les maximuns horizontals de, on utilise A.max(axis=1) :",A.max(axis=1))

print("")
print("Pour avoir les indices des minimuns vericals de A, on utilise, A.argmin(axis=0) :",A.argmin(axis=0))
print("Pour avoir les indices des maximuns vericals de A, on utilise, A.argmax(axis=0) :",A.argmax(axis=0))
print("Pour avoir les indices des minimuns horizontals de A, on utilise, A.argmin(axis=1) :",A.argmin(axis=1))
print("Pour avoir les indices des maximuns horizontals de A, on utilise, A.argmax(axis=1) :",A.argmax(axis=1))
print("")

#Tri
print("")
print("Tri")

B=np.array([[3, 1, 6, 2, 4],
            [1, 5, 9, 0, 2]])

print("B =")
print(B)

C=B.copy()
C=np.sort(C,axis=0)
D=B.copy()
D=np.sort(D,axis=1)
C1=B.copy()

E=B.copy()
E=np.argsort(E,axis=0)
F=B.copy()
F=np.argsort(F,axis=1)

#np.sort(axis=0)
print("")
print("#np.sort(axis=0)")

print("")
print("Pour avoir le tableau B trié par rapport à l'axe vertical, on utilise C=np.sort(B,axis=0) :")
print(C)

print("")
print("Pour avoir le tableau B trié par aux indices de l'axe vertical, on utilise C=np.argsort(B,axis=0) :")
print(E)


#np.sort(axis=1)
print("")
print("#np.sort(axis=1)")

print("")
print("Pour avoir le tableau B trié par rapport à l'axe horizontal, on utilise C=np.sort(B,axis=1) :")
print(D)

print("")
print("Pour avoir le tableau B trié par aux indices de l'axe horizontal, on utilise C=np.argsort(B,axis=01) :")
print(F)

print("")
print("[[3=0, 1=1, 6=2, 2=3, 4=4],",'\n',
       "[1=0, 5=1, 9=2, 0=3, 2=4]]")

#Statistique
print("")
print("Statistique")

print("Pour avoir la moyenne de A, on utilise A.mean() :",A.mean())
print("Pour avoir la moyenne de l'axe vertical, on utilise A.mean(axis=0) :",A.mean(axis=0))
print("Pour avoir la moyenne de l'axe horizontal, on utilise A.mean(axis=1) :",A.mean(axis=1))

print("")
print("Pour avoir l'écat type de A, on utilise",A.std())
print("Pour avoir l'écat type de l'axe vertical, on utilise A.std(axis=0) :",A.std(axis=0))
print("Pour avoir l'écat type de l'axe horizontal, on utilise A.std(axis=1) :",A.std(axis=1))

print("")
print("Pour avoir la variance de A est ",A.var())
print("Pour avoir la variance de l'axe vertical, on utilise A.var(axis=0) :",A.var(axis=0))
print("Pour avoir la variance de l'axe horizontal, on utilise A.var(axis=1) :",A.var(axis=1))

G=np.corrcoef(B)
H=np.corrcoef(B)[0,1]

print("")
print("La matrice de corélation de B vaut")
print(G)

print("")
print("Le nombre de la matrice de corélation situé à la première ligne, deuxième cologne vaut")
print(H)

print("")
print("Le tableau affichant le nombre de fois qu'un nombre apparrait ",np.unique(B,return_counts=True))
print("Liste des nombres \t     ",np.unique(B,return_counts=True)[0])
print("Nombre de leurs apparaissiont",np.unique(B,return_counts=True)[1])

#Code de trie
print("")
print("#Code de trie")
values, counts =np.unique(B,return_counts=True)
for i,j in zip (values[counts.argsort()],counts[counts.argsort()]):
    print(f'valeur {i} apparait {j}')

#Not a Number
print("")
print("#Not a Number")

I=np.random.randn(5,5)
I[1,2]=np.nan
I[4,1]=np.nan
I[3,3]=np.nan
print("Tableau corrompu")
print(I)

print("")
print("Il faut utiliser np.nanmean(I) pour calculer la moyenne",np.nanmean(I))
print("Il faut utiliser np.nansdt(I) pour calculer l'écat type",np.nanstd(I))
print("Il faut utiliser np.nanvar(I) pour calculer la variance",np.nanvar(I))

print("")
print("Il faut utiliser np.nanmean(I,axis=0)) pour calculer la moyenne de l'axe vertical \n",np.nanmean(I,axis=0))
print("Il faut utiliser np.nansdt(I,axis=0)) pour calculer l'écat type de l'axe vertical \n",np.nanstd(I,axis=0))
print("Il faut utiliser np.nanvar(I,axis=0)) pour calculer la variance de l'axe vertical \n",np.nanvar(I,axis=0))

print("")
print("Il faut utiliser np.nanmean(I,axis=1)) pour calculer la moyenne de l'axe horizontal \n",np.nanmean(I,axis=1))
print("Il faut utiliser np.nansdt (I,axis=1)) pour calculer l'écat type de l'axe horizontal \n",np.nanstd(I,axis=1))
print("Il faut utiliser np.nanvar (I,axis=1)) pour calculer la variance de l'axe horizontal \n",np.nanvar(I,axis=1))

print("")
print("Il faut utiliser np.isnan(I) pour avoir un masque de la matrice affichant si l'object est un nombre ou un nan ")
print(np.isnan(I))

print("")
print("Il faut utiliser np.isnan(I).sum() pour le nombre de nan dans la matrice")
print("Il y a ",np.isnan(I).sum()," dans la matrice")

print("")
print("Pour corriger le problème on peut faire du boolean indexing I[np.isnan(I)]=0")
I[np.isnan(I)]=0
print(I)

#Algèbre Linèaire
print("")
print("#Algèbre Linèaire")

J=np.random.randn(2,3)
print("J vaut ")
print(J)
print("La forme de J vaut",J.shape)

print("")
J=J.T
print("La transposé de J vaut ")
print(J)
print("La forme de la tranposé deJ vaut",J.shape)

print("")
print("Pour faire le produit matricielle on utilise A.dot(B)")
print("Donc H=J.dot(J.T) est égale")
H=J.dot(J.T)
print(H)
