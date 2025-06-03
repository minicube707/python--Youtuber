import numpy as np
import matplotlib.pyplot as plt
from sklearn. cluster import KMeans
from sklearn.datasets import make_blobs, load_digits
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
import warnings

# Ignorer les UserWarnings
warnings.filterwarnings("ignore", category=UserWarning)

# Génération de données
X, y = make_blobs(n_samples=100, centers=3, cluster_std=0.4, random_state=0)

print("\nX",X)
print("\ny",y)
#Fonction
def function_found_nb_cluster(list_inertia):

    i=0
    nb_cluster = 1
    while i <=(len(list_inertia)-2):

        f_ele=list_inertia[i]
        s_ele=list_inertia[i+1]

        if np.abs(f_ele-s_ele)<10:
            nb_cluster=i+1
            i=len(list_inertia)

        else:
            i+=1

    return nb_cluster


#Algorythme
plt.figure()
plt.title("Data_set")
plt.scatter(X[:,0], X[:,1])
plt.show()

#n_clusters: nombre de cluster
#n_init: nombre d'éxécution(10)
#max_iter: nombred'itératoin(300)
#init: stratégie dinitialisation
nb_cluster=3
model= KMeans(n_clusters=nb_cluster, n_init='auto')
model.fit(X)

print("")
print("L'inertia est de ",model.inertia_)

#Comment sont classée nos différent échantillions
tab_label=model.labels_
print(tab_label)

tab_clusters=model.cluster_centers_

print("")
print("Position des clusteur:\n",tab_clusters)

#Affichage des coordonnées par cluster
print("")
for i in range(tab_clusters.shape[0]):
    ligne_cluster=tab_clusters[i,:]
    print(f"Cluster N°{i} aux coordonné X:{ligne_cluster[0]} et Y:{ligne_cluster[1]}")


X_cluster=tab_clusters[:,0]
Y_cluster=tab_clusters[:,1]

plt.figure()
plt.title("Data rassemblé par groupe")
plt.scatter(X[:,0], X[:,1], c=model.labels_, label=("data"))
plt.scatter(X_cluster, Y_cluster, c='r', label=("Clusteur"))
plt.legend()
plt.show()

#Affichage des datas par clusteurs
for i in range(nb_cluster):

    ligne_cluster=tab_clusters[i,:]
    label_data=X[tab_label==i]

    plt.figure()
    plt.title(f"Data du cluster N°{i}")
    plt.scatter(label_data[:,0], label_data[:,1], label=("Data"))
    plt.scatter(ligne_cluster[0], ligne_cluster[1], c='r', label=("Cluster"))
    plt.legend()
    plt.show()

#Comment savoir le nombre de clusters à mettre pour notre data_set
#Nous allons utiliser la méthode de la zone de coude 

for i in range(1,4):

    X, y = make_blobs(n_samples=100, centers=np.random.randint(1,10), cluster_std=0.4, random_state=0)

    plt.figure()
    plt.title(f"Data_set N°{i}")
    plt.scatter(X[:,0], X[:,1])
    plt.show()

    list_inertia=[]
    max_cluster=10
    n=np.arange(1,max_cluster,1)

    print("")
    for i in n:

        model=KMeans(n_clusters=i, n_init='auto')
        model.fit(X)

        inertia=model.inertia_
        print("Inertia=",inertia)
        list_inertia.append(inertia)

    plt.figure()
    plt.plot(n, list_inertia)
    plt.xlabel('nombre de clusters')
    plt.ylabel('Cout du modele (Inertia)')
    plt.show()

    nb_cluster=function_found_nb_cluster(list_inertia)

    print("")
    print("Le nombre de clusters est ", nb_cluster)

    model= KMeans(n_clusters=nb_cluster, n_init='auto')
    model.fit(X)

    tab_clusters=model.cluster_centers_

    print("")
    print("Position des clusteur:\n",tab_clusters)

    X_cluster=tab_clusters[:,0]
    Y_cluster=tab_clusters[:,1]

    plt.figure()
    plt.title("Data rassemblé par groupe")
    plt.scatter(X[:,0], X[:,1], c=model.labels_, label="data")
    plt.scatter(X_cluster, Y_cluster, c='r', label="Clusteur")
    plt.legend()
    plt.show()


#Recherche d'anomaile

X, y = make_blobs(n_samples=50, centers=1, cluster_std=0.1, random_state=0)
X[-1,:] = np.array([2.25, 5])

plt.figure()
plt.title("Data avec anomalie")
plt.scatter(X[:,0], X[:,1])
plt.show()

#contamination=Le nombre d'anomalie dans notre data_set
model=IsolationForest(contamination=0.1)
model.fit(X)
label_anomalie=model.predict(X)

plt.figure()
plt.title("Data avec anomalie trouvée")
plt.scatter(X[:,0], X[:,1], c=label_anomalie)
plt.show()

#Valeurs normale=1, anomaile=-1 
print("")
print("list des anomalies=", label_anomalie)

data=X[label_anomalie==1]
anomalie=X[label_anomalie==-1]

plt.figure()
plt.title("Data sans anomalie")
plt.scatter(data[:,0], data[:,1], label=("Data"))
plt.legend()

plt.figure()
plt.title("Anomalie sans data")
plt.scatter(anomalie[:,0], anomalie[:,1], label=("Anomalie"))
plt.legend()
plt.show()


#Application Décontamination Digits

digits = load_digits()
images = digits.images
X = digits.data
y = digits.target

plt.figure()
plt.title(f"Image du chiffre N°{y[0]}")
plt.imshow(images[0])
plt.show()

print("")
print("X.shape=", X.shape)

model=IsolationForest(random_state=0, contamination=0.02)
model.fit(X)
outlier = model.predict(X) == -1

print("")
print("Filtre des bons chiffre")
print(model.predict(X))

plt.figure()
plt.title(f"Image du chiffre anomalie N°{y[outlier][0]}")
plt.imshow(images[outlier][0])
plt.show()

#Réduction de dimension
#Le but est de réduire la complexité superflue d'un dataset en projetant ses données dans un espace de plus petite dimension
#(un espace avec moins de variable)
#Ceci dans le but d'accélérer l'aprentisage de la machine et d'éviter 'le fléau de la dimension' (risque d'overfitting)

#Le principe est de projeter nos données sur des axes  appelés 'Composantes Principales', en cherchant à minimiser la distance
#entre nos point et leurs projection
#Ainsi, on réduit la dimension  de notre dataset, tout en préservant au maximun la variance de nos données

#Pour trouver les axes de projection:
#1: On calcule la matrice  de covariance des  données
#2: On détermines les vecteurs propres de cette matrice: ce sont les 'Composantes Principales'
#": On projectte les données sur ces axes"

#Avant d'utiliser PCA, il faut Standardiser les données avec StandarScalar()
#PCA n'est pas efficace sur le datasets non-linéaire
#Pca est normalement conçu pour traiter les variables continues

#Une variable continue est une variable qui peut prendre une infinité de valeurs possibles dans un certain intervalle.
#Elle peut être mesurée avec n'importe quelle précision souhaitée.
#Par exemple, la taille, le poids, la température, la vitesse, etc., sont des exemples de variables continues.
#Elles peuvent prendre des valeurs fractionnaires et il existe une infinité de valeurs entre deux points donnés.

#En revanche, une variable discrète est une variable qui ne peut prendre que des valeurs spécifiques, distinctes et isolées.
#Elle ne peut pas prendre de valeurs fractionnaires et il existe un nombre fini ou dénombrable de valeurs possibles.
#Par exemple, le nombre de personnes dans une famille, le nombre de voitures dans un parking,
#le nombre de téléphones dans un foyer, etc., sont des exemples de variables discrètes.



#Visualisation de données en 2D

#PCA est un transformer
model=PCA(n_components=2)
X_reduced=model.fit_transform(X)

print("")
print("Les dimension sont maintenant de ",X_reduced.shape)

plt.figure()
plt.title("Spatialisation des chiffres en 2D")
plt.scatter(X_reduced[:,0], X_reduced[:,1], c=y)
plt.colorbar()
plt.show()

plt.figure()
plt.title("Spatialisation des chiffres en 2D")
plt.xlim(-30, 30)
plt.ylim(-30, 30)

for i in range(100):
    plt.text(X_reduced[i,0], X_reduced[i,1], str(y[i]))
plt.show()

print("")
print("La Matrice de passage",model.components_.shape)
print(model.components_)

#Compression de données
#Permet d'accélerer l'apprentissage de la machine toutes en conservant nos données

model=PCA(n_components=X.shape[1])
X_reduced=model.fit_transform(X)

sum_var=np.cumsum(model.explained_variance_ratio_)

print("")
print("Somme cumulé de la variance:\n",sum_var)

plt.figure()
plt.plot(range(0,sum_var.size), sum_var)
plt.title("Graphique montrant l'évolution\n entre le nombre de dimension et la variance")
plt.xlabel("Nombre de dimension")
plt.ylabel("Pourcentage de la variance")
plt.show()

max_var=0.99
indice_var=np.argmax(np.cumsum(model.explained_variance_ratio_)> max_var)

print("")
print(f"C'est à de l'indice {indice_var} que la variance est supérieur à {max_var}")

#Pour afficher les données une fois compressé
model=PCA(n_components=indice_var)
X_reduced=model.fit_transform(X)

plt.figure()
plt.title("Chiffre compressé")
plt.imshow(X_reduced[0].reshape((8,5)))
plt.show()

X_recover=model.inverse_transform(X_reduced)

plt.figure()
plt.title("Chiffre décompressé")
plt.imshow(X_recover[0].reshape((8,8)))
plt.show()