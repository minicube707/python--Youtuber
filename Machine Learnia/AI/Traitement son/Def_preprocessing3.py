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
def normalize_to_range(data, new_min, new_max):
    min_val = np.min(data)
    max_val = np.max(data)

    # Formule de normalisation min-max
    if all(element == data[0] for element in data) == True:
        normalized_data = np.zeros(len(data))
    else:
        normalized_data = ((data - min_val) / (max_val - min_val)) * (new_max - new_min) + new_min

    return normalized_data


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

            print("")
            if Y[masque_max][i] < Y[masque_max][i+1]:
                
                print("Premier plus petit que deuxième")
                print("i=",i)
                print("Y[masque_max][i]=", Y[masque_max][i])
                print("Y[masque_max][i+1]=", Y[masque_max][i+1])
                print("Before delete masque_max\n",masque_max)
                print("Y[masque_max]\n",Y[masque_max])

                masque_max = np.delete(masque_max, i-1)
                list_max_del = np.append(list_max_del, i-1)

                print("")
                print("After delete masque_max\n",masque_max)
                print("Y[masque_max]\n",Y[masque_max])
                print("list_max_del",list_max_del)

            else:

                print("i=",i)
                print("Y[masque_max][i]=", Y[masque_max][i])
                print("Y[masque_max][i+1]=", Y[masque_max][i+1])
                print("Deuxièeme plus petit que premier")
                print("Before delete masque_max\n",masque_max)

                masque_max = np.delete(masque_max, i+1)
                list_max_del = np.append(list_max_del, i+1)

                print("After delete masque_max\n",masque_max)
                print("list_max_del",list_max_del)

            masque_min = np.delete(masque_min, i)
            list_min_del = np.append(list_min_del, i)
    """
    print("")
    print("masque_min.size",masque_min.size)
    print("masque_min",masque_min)

    print("")
    print("masque_max.size",masque_max.size)
    print("masque_max",masque_max)

    print("")
    print("list_min_del.size",list_min_del.size)
    print("list_min_del",list_min_del)

    print("")
    print("list_max_del.size",list_max_del.size)
    print("list_max_del",list_max_del)
    """

    N2 = np.array([])
    NA2 = np.array([])

    i=0
    a=0

    list_intervalle_min = np.array([], dtype=int)
    list_intervalle_max = np.array([], dtype=int)

    while a <=  masque_max.size-1:
        print("")
        print("list_intervalle_min",list_intervalle_min)
        print("list_intervalle_max",list_intervalle_max)
        intervalle = 0
        if i%2 == 0:
            
            if a not in list_min_del:
                print("min")
                print("masque_min[a]",masque_min[a])
                print("masque_max[a]",masque_max[a])
                print("X[masque_min[a]:masque_max[a]]", X[masque_min[a]:masque_max[a]])
                print("Y[masque_min[a]:masque_max[a]]", Y[masque_min[a]:masque_max[a]])

                N2 = np.append(N2, X[masque_min[a]:masque_max[a]])
                NA2 = np.append(NA2, Y[masque_min[a]:masque_max[a]])

                list_intervalle_min = np.append(list_intervalle_min, intervalle)

            else:
                intervalle = X[masque_min[a]:masque_max[a]+1].size
                list_intervalle_min = np.append(list_intervalle_min, intervalle)
                
        else:
            if a not in list_max_del:
                print("max")
                print("masque_min[a+1]",masque_min[a+1])
                print("masque_max[a]",masque_max[a])
                print("X[masque_max[a]:masque_min[a+1]]", X[masque_max[a]:masque_min[a+1]])
                print("Y[masque_max[a]:masque_min[a+1]]", Y[masque_max[a]:masque_min[a+1]])

                N2 = np.append(N2, X[masque_max[a]:masque_min[a+1]])
                NA2 = np.append(NA2, Y[masque_max[a]:masque_min[a+1]])

                list_intervalle_max = np.append(list_intervalle_max, intervalle)

            else:
                intervalle = X[masque_max[a]:masque_min[a+1]+1].size
                list_intervalle_max = np.append(list_intervalle_max, intervalle)

            a+=1
            print("a=",a)
        i+=1


    inter = 0
    new_masque_max = np.array([], dtype=int)

    for i in range(list_intervalle_max.size):
        inter = inter + list_intervalle_max[i]
        new_masque_max = np.append(new_masque_max, masque_max[i]-inter)

    inter = 0
    new_masque_min = np.array([], dtype=int)

    for i in range(list_intervalle_min.size):
        inter = inter + list_intervalle_min[i]
        new_masque_min = np.append(new_masque_min, masque_min[i]-inter)

    N2 = np.append(N2, X[-1])
    NA2 = np.append(NA2, Y[-1])

    return N2, NA2, new_masque_min, new_masque_max


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


    



