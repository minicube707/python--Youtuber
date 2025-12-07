import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import argrelextrema 


def function_vecteur (list_indice_min, list_indice_max, X, Y, pourcent):

    a=0
    b=0

    list_ordonnée_vecteur = np.array([])   
    list_abscisse_vecteur = np.array([])   

    list_ordonnée_vecteur = np.append(list_ordonnée_vecteur, 0)
    list_abscisse_vecteur = np.append(list_abscisse_vecteur, 0)

    if (pourcent<0) or (pourcent>1):
        raise ValueError ("Pourcent doit être compris entre 0 et 1 inclue")


    for i in range(list_indice_min.size + list_indice_max.size -1):
        
        vecteur = Y[list_indice_min[a]] - Y[list_indice_max[b]]

        if i%2!=0: #Max à Min

            list_ordonnée_vecteur = np.append(list_ordonnée_vecteur, vecteur) 
            list_abscisse_vecteur = np.append(list_abscisse_vecteur, X[ a+b ]*-1)

            b+=1
        
        else: #Min à Max
            vecteur = vecteur*(-1)

            list_ordonnée_vecteur = np.append(list_ordonnée_vecteur, vecteur) 
            list_abscisse_vecteur = np.append(list_abscisse_vecteur, X[ a+b ])
    
            a+=1

    list_ordonnée_vecteur_argument_sort = np.argsort(np.abs(list_ordonnée_vecteur))
    list_ordonnée_vecteur_ones = np.zeros((list_ordonnée_vecteur.shape))  
 
    a=0

    for i in range( int(( list_abscisse_vecteur.size * (1-pourcent)))):       #Les zeros serviront de point normal par rapport au -1 qui permeteront d'avoir les plus grandes valeurs 

        a = list_ordonnée_vecteur_argument_sort[i]
        list_ordonnée_vecteur_ones[a] = -1

    list_ordonnée_vecteur_ones[0] = 0

    masque =np.array(list_ordonnée_vecteur_ones == 0)

    """
    print("\nmasque.shape",masque.shape)
    print("masque.size",masque.size)
    print("masque",masque)

    print("\nlist_ordonnée_vecteur.shape:",list_ordonnée_vecteur.shape)
    print("list_ordonnée_vecteur.size:",list_ordonnée_vecteur.size)
    print("list_ordonnée_vecteur:",list_ordonnée_vecteur)

    print("\nlist_abscisse_vecteur.shape:",list_abscisse_vecteur.shape)
    print("list_abscisse_vecteur.size:",list_abscisse_vecteur.size)
    print("list_abscise_vecteur:",list_abscisse_vecteur)
    """

    list_abscisse = np.array([list_indice_min, list_indice_max]).flatten('F')
    list_ordonnée = np.array([Y[list_indice_min], Y[list_indice_max]]).flatten('F')

    """
    print("\nlist_abscisse.shape", list_abscisse.shape) 
    print("list_abscisse.size", list_abscisse.size)
    print("list_abscisse", list_abscisse)
    """

    new_list_ordonnée_vecteur = np.abs(list_ordonnée)[masque]
    new_list_abscisse_vecteur = np.abs(list_abscisse)[masque]

    """
    print("\nlist_ordonnée_vecteur.shape:",new_list_ordonnée_vecteur.shape)
    print("list_ordonnée_vecteur_.size:",new_list_ordonnée_vecteur.size)
    print("list_ordonnée_vecteur:",new_list_ordonnée_vecteur)

    print("\nnew_list_abscisse_vecteur.shape:",new_list_abscisse_vecteur.shape)
    print("new_list_abscisse_vecteur.size:",new_list_abscisse_vecteur.size)
    print("new_list_abscisse_vecteur:",new_list_abscisse_vecteur)
    """
    return new_list_abscisse_vecteur, new_list_ordonnée_vecteur, masque


