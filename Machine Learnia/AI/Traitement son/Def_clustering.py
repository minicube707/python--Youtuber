import numpy as np
from sklearn. cluster import KMeans, SpectralClustering, AffinityPropagation

import matplotlib.pyplot as plt

def fonction_clustering_KMeans(X, seuil):

    max_cluster=10
    range_cluster=np.arange(1,max_cluster,1)

    print("")
    for i in range_cluster:

        model=KMeans(n_clusters=i, n_init=10, init='k-means++')
        model.fit(X)

        inertia=model.inertia_
        print("Inertia=",inertia)

        if inertia < seuil:
            break


    print("")
    print("Le nombre de clusters est ", i)

    model= KMeans(n_clusters=i, n_init=10, init='k-means++')
    model.fit(X)

    return model.cluster_centers_, model.labels_


def fonction_clustering_Spectral(X, NA, M):

    max_cluster=10
    range_cluster=np.arange(1,max_cluster,1)

    print("")
    for i in range_cluster:

        model= SpectralClustering(n_clusters=i, affinity='nearest_neighbors', eigen_solver='arpack', assign_labels ="kmeans")
        labels_spectral = model.fit_predict(X)
        print("")
        print(f"X{i}\n",labels_spectral)

        plt.figure()
        plt.plot(np.arange(NA.size), NA)
        plt.scatter(np.arange(NA.size)[M], NA[M], c=labels_spectral)
        plt.show()

    return  model.labels_


def fonction_clustering_AffinityPropagation(X):

    model = AffinityPropagation()
    model.fit(X)


    return  model.cluster_centers_, model.labels_

