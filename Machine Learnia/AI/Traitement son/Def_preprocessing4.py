import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

from sklearn.preprocessing import RobustScaler
from Def_graphique import fonction_graphque_comparaison
import os

os.chdir("C:\\Users\\flore\\Desktop\\Document\\Programme\\Python\\AI\\Traitement son")


"""New Fonction"""
def function_difference_tangente (list_indice_min, list_indice_max, X, Y, pourcent):

    a=0
    b=0

    list_tangente = np.array([])     
    list_tangente = np.append(list_tangente, 0)

    list_ordonnee = np.array([])
    list_abscisse = np.array([])

    if (pourcent<0) or (pourcent>1):
        raise ValueError ("Pourcent doit être compris entre 0 et 1 inclue")


    for i in range(list_indice_min.size + list_indice_max.size -1):
        
        list_ordonnee = np.append(list_ordonnee, Y[list_indice_min[a]] - Y[list_indice_max[b]])
        list_abscisse = np.append(list_abscisse ,X[list_indice_min[a]] - X[list_indice_max[b]])

    
        if i%2!=0: #Max à Min
            b+=1
        
        else: #Min à Max
            a+=1

    list_ordonnee_robscal = RobustScaler().fit_transform(list_ordonnee.reshape(-1, 1))
    list_abscisse_robscal = RobustScaler().fit_transform(list_abscisse.reshape(-1, 1))

    list_tangente = np.sqrt(np.abs(list_ordonnee_robscal)**2 + np.abs(list_abscisse_robscal)**2)
    list_tangente = list_tangente.reshape(1, -1)
    list_tangente = list_tangente[0]


    list_ordonnée_vecteur_argument_sort = np.argsort(list_tangente)       
    list_ordonnée_vecteur_ones = np.zeros((list_tangente.shape))                
    a=0

    for i in range( int(( list_tangente.size * (1-pourcent)))):       #Les zeros serviront de point normal par rapport au -1 qui permeteront d'avoir les plus petites valeurs 

        a = list_ordonnée_vecteur_argument_sort[i]
        list_ordonnée_vecteur_ones[a] = -1

    list_ordonnée_vecteur_ones[0] = 0

    masque =np.array(list_ordonnée_vecteur_ones == 0)
    masque = np.append(masque, True)

    list_abscisse = np.array([X[list_indice_min], X[list_indice_max]]).flatten('F')
    list_ordonnée = np.array([Y[list_indice_min], Y[list_indice_max]]).flatten('F')

    new_list_ordonnée_vecteur = np.abs(list_ordonnée)[masque]
    new_list_abscisse_vecteur = np.abs(list_abscisse)[masque]

    return new_list_abscisse_vecteur, new_list_ordonnée_vecteur, masque


"""New Fonction"""
def function_difference_verticale (list_indice_min, list_indice_max, X, Y, pourcent):

    a=0
    b=0

    list_tangente = np.array([])     
    list_tangente = np.append(list_tangente, 0)

    list_ordonnee = np.array([])

    if (pourcent<0) or (pourcent>1):
        raise ValueError ("Pourcent doit être compris entre 0 et 1 inclue")


    for i in range(list_indice_min.size + list_indice_max.size -1):
        
        list_ordonnee = np.append(list_ordonnee, Y[list_indice_min[a]] - Y[list_indice_max[b]])

        if i%2!=0: #Max à Min
            b+=1
        
        else: #Min à Max
            a+=1

    list_ordonnee_robscal = RobustScaler().fit_transform(list_ordonnee.reshape(-1, 1))

    list_tangente = list_ordonnee_robscal
    list_tangente = list_tangente.reshape(1, -1)
    list_tangente = list_tangente[0]


    list_ordonnée_vecteur_argument_sort = np.argsort(list_tangente)       
    list_ordonnée_vecteur_ones = np.zeros((list_tangente.shape))                
    a=0

    for i in range( int(( list_tangente.size * (1-pourcent)))):       #Les zeros serviront de point normal par rapport au -1 qui permeteront d'avoir les plus petites valeurs 

        a = list_ordonnée_vecteur_argument_sort[i]
        list_ordonnée_vecteur_ones[a] = -1

    list_ordonnée_vecteur_ones[0] = 0

    masque =np.array(list_ordonnée_vecteur_ones == 0)
    masque = np.append(masque, True)

    list_abscisse = np.array([X[list_indice_min], X[list_indice_max]]).flatten('F')
    list_ordonnée = np.array([Y[list_indice_min], Y[list_indice_max]]).flatten('F')

    new_list_ordonnée_vecteur = np.abs(list_ordonnée)[masque]
    new_list_abscisse_vecteur = np.abs(list_abscisse)[masque]

    return new_list_abscisse_vecteur, new_list_ordonnée_vecteur, masque


"""New Fonction"""
def function_difference_horizon (list_indice_min, list_indice_max, X, Y, pourcent):

    a=0
    b=0

    list_tangente = np.array([])     
    list_tangente = np.append(list_tangente, 0)

    list_abscisse = np.array([])

    if (pourcent<0) or (pourcent>1):
        raise ValueError ("Pourcent doit être compris entre 0 et 1 inclue")


    for i in range(list_indice_min.size + list_indice_max.size -1):
        
        list_abscisse = np.append(list_abscisse, X[list_indice_min[a]] - X[list_indice_max[b]])

        if i%2!=0: #Max à Min
            b+=1
        
        else: #Min à Max
            a+=1

    list_abscisse_robscal = RobustScaler().fit_transform(list_abscisse.reshape(-1, 1))

    list_tangente = list_abscisse_robscal
    list_tangente = list_tangente.reshape(1, -1)
    list_tangente = list_tangente[0]


    list_ordonnée_vecteur_argument_sort = np.argsort(list_tangente)       
    list_ordonnée_vecteur_ones = np.zeros((list_tangente.shape))                
    a=0

    for i in range( int(( list_tangente.size * (1-pourcent)))):       #Les zeros serviront de point normal par rapport au -1 qui permeteront d'avoir les plus petites valeurs 

        a = list_ordonnée_vecteur_argument_sort[i]
        list_ordonnée_vecteur_ones[a] = -1

    list_ordonnée_vecteur_ones[0] = 0

    masque =np.array(list_ordonnée_vecteur_ones == 0)
    masque = np.append(masque, True)

    list_abscisse = np.array([X[list_indice_min], X[list_indice_max]]).flatten('F')
    list_ordonnée = np.array([Y[list_indice_min], Y[list_indice_max]]).flatten('F')

    new_list_ordonnée_vecteur = np.abs(list_ordonnée)[masque]
    new_list_abscisse_vecteur = np.abs(list_abscisse)[masque]

    return new_list_abscisse_vecteur, new_list_ordonnée_vecteur, masque


"""New Fonction"""
def fonction_trouver_suites_occurentes(liste, longueur_suite):
    suites_occurentes = defaultdict(int)
    fin_liste = len(liste) - longueur_suite + 1

    for i in range(fin_liste):
        suite = tuple(liste[i:i+longueur_suite])
        suites_occurentes[suite] += 1

    return {k: v for k, v in suites_occurentes.items() if v > 1}



"""New Fonction"""
def normalize_to_range(data):
    
    # Supposons que vos coordonnées sont stockées dans un tableau numpy 'points'
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)

    # Normalisation
    normalized_points = (data - mean) / std

    return normalized_points


"""New Fonction"""
def fonction_trouver_max_plus_grand(main_liste, liste_valeur, liste_indice, intervalle=50):
    resultats = []

    for a in range(len(liste_valeur)):

        i = int(liste_indice[a])
        valeur = liste_valeur[a]
  
        max_plus_grand_indice = i
        max_plus_grand_valeur = valeur

        for j in range(i - intervalle, i + intervalle+1):
            try:

                if j != i and main_liste[j] > max_plus_grand_valeur:
                    max_plus_grand_valeur = main_liste[j]
                    max_plus_grand_indice = j

            except:
                break

        info_point = {
            "indice": i,
            "valeur": valeur,
            "max_plus_grand_indice": max_plus_grand_indice,
            "max_plus_grand_valeur": max_plus_grand_valeur,
            "max_plus_grand_present": max_plus_grand_indice != -1 and max_plus_grand_valeur > valeur,
        }

        resultats.append(info_point)

    return resultats


"""New Fonction"""
def fonction_trouver_min_plus_petit(main_liste, liste_valeur, liste_indice, intervalle=50):
    resultats = []

    for a in range(len(liste_valeur)):
        i = int(liste_indice[a])
        valeur = liste_valeur[a]

        min_plus_petit_indice = i
        min_plus_petit_valeur = valeur

        for j in range(i - intervalle, i + intervalle+1):
            try:

                if j != i and main_liste[j] < min_plus_petit_valeur:
                    min_plus_petit_valeur = main_liste[j]
                    min_plus_petit_indice = j

            except:
                break

        info_point = {
            "indice": i,
            "valeur": valeur,
            "min_plus_petit_indice": min_plus_petit_indice,
            "min_plus_petit_valeur": min_plus_petit_valeur,
            "min_plus_petit_present": min_plus_petit_indice != -1 and min_plus_petit_valeur < valeur,
        }

        resultats.append(info_point)

    return resultats


"""New Fonction"""
def fonction_smooth(masque_min, masque_max, X, Y, intervalle=100):

    list_min_del = np.array([], dtype=int)
    list_max_del = np.array([], dtype=int)

    for i in range(X[masque_max].size-2):
            if np.abs(X[masque_max][i] - X[masque_max][i+1]) < intervalle:

                if Y[masque_max][i] < Y[masque_max][i+1]:
                    list_max_del = np.append(list_max_del, i)

                else:
                    list_max_del = np.append(list_max_del, i+1)

                list_min_del = np.append(list_min_del, i+1)

 
    N2 = np.array([], dtype=int)
    NA2 = np.array([] , dtype=int)

    i=0
    a=0
    while a <=  masque_max.size-1:
        if i%2 == 0:
            
            if a not in list_min_del:

                N2 = np.append(N2, X[masque_min[a]:masque_max[a]])
                NA2 = np.append(NA2, Y[masque_min[a]:masque_max[a]])
       
        else:
            if a not in list_max_del:

                N2 = np.append(N2, X[masque_max[a]:masque_min[a+1]])
                NA2 = np.append(NA2, Y[masque_max[a]:masque_min[a+1]])

            a+=1
        i+=1

    N2 = np.append(N2, X[-1])
    NA2 = np.append(NA2, Y[-1])

    return N2, NA2


"""New Fonction"""
def fonction_aligne(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    X = np.array([point1[0], point2[0], point3[0]])
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)

    # Normalisation
    X_norm = (X - mean) / std
    x1 = X_norm[0]
    x2 = X_norm[1]
    x3 = X_norm[2]

    Y = np.array([point1[1], point2[1], point3[1]])
    mean = np.mean(Y, axis=0)
    std = np.std(Y, axis=0)

    # Normalisation
    Y_norm = (Y - mean) / std
    y1 = Y_norm[0]
    y2 = Y_norm[1]
    y3 = Y_norm[2]


    produit_croix = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)

    return abs(produit_croix) < 1  # Utiliser une petite tolérance pour tenir compte des erreurs d'arrondi


"""New Fonction"""
def fonction_straight(X, Y):

    New_X = np.array([], dtype=int)
    New_Y = np.array([], dtype=int)

    i=0
    intervalle =0
    while i < X.size-3:

        point1 = [X[i], Y[i]]
        point2 = [X[i + 1 + intervalle], Y[i + 1 + intervalle]]
        point3 = [X[i + 2 + intervalle], Y[i + 2 + intervalle]]

        res = fonction_aligne(point1, point2, point3)
        
        if res == False:
            New_X = np.append(New_X, X[i])
            New_Y = np.append(New_Y, Y[i])
            i+= 1 + intervalle
            intervalle = 0
        else:
            intervalle +=1
            
    New_X = np.append(New_X, point2[0])
    New_Y = np.append(New_Y, point2[1])

    New_X = np.append(New_X, point3[0])
    New_Y = np.append(New_Y, point3[1])

    New_X = np.append(New_X, X[-1])
    New_Y = np.append(New_Y, Y[-1])
                      
    return New_X, New_Y



if __name__ =="__main__":

    data = np.loadtxt("Data.txt")
    data = np.array(data).astype(int)

    min = np.loadtxt("Min.txt")
    max = np.loadtxt("Max.txt")
    min = np.array(min).astype(int)
    max = np.array(max).astype(int)
    

    print("")
    print("data.size", data.size)
    print("")
    print("max", max)
    print("")
    print("min", min)

    n = np.arange(data.size)
    
    XX, YY, M = function_difference_tangente(min, max, n, data, 0.25)

    YY = np.append(YY, data[-1])
    XX = np.append(XX, data.size-1)

    X=[np.arange(data.size), XX]
    Y=[data, YY]
    fonction_graphque_comparaison(X, Y, genre=["plot", "plot"], label_graph=["Fichier original", "Preprocesing N°1"])

    """
    print("")
    print("test")
    print("masque",M)
    print("")
    print("M Impair",M[0::2])
    print("M pair", M[1::2])
    """


    



