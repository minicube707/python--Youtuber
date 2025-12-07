import numpy as np
import matplotlib.pyplot as plt

def batage(listmin, listmax):

    a=0
    list=[]

    if (len(listmin) + len(listmax)) % 2 ==0:
        while a < (len(listmin)):

            list.append(listmin[a])
            list.append(listmax[a])
            a+=1

    else:
        while a < (len(listmax)):

            list.append(listmin[a])
            list.append(listmax[a])
            a+=1

        list.append(listmin[a])

    return np.array(list)

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
            list_abscisse_vecteur = np.append(list_abscisse_vecteur, X[ a+b ])

            b+=1
        
        else: #Min à Max
            vecteur = vecteur*(-1)

            list_ordonnée_vecteur = np.append(list_ordonnée_vecteur, vecteur) 
            list_abscisse_vecteur = np.append(list_abscisse_vecteur, X[ a+b ]*-1)
    
            a+=1

    list_ordonnée_vecteur_argument_sort = np.argsort(np.abs(list_ordonnée_vecteur))[::-1]   #Le [::-1] sert pour avoir la list dans l'ordre décroissant
    list_ordonnée_vecteur_zeros = np.zeros((list_ordonnée_vecteur.shape))                   #Les zeros serviront de point normal par rapport au 1 qui permeteront d'avoir les plus grandes valeurs       
    a=0

    for i in range( int(( list_abscisse_vecteur.size ) * pourcent)):

        a = list_ordonnée_vecteur_argument_sort[i]
        list_ordonnée_vecteur_zeros[a] = 1

    list_ordonnée_vecteur_zeros[0] = 1
    
    """
    print("\nlist_ordonnée_vecteur_zeros:",list_ordonnée_vecteur_zeros)
    """

    masque =np.array(list_ordonnée_vecteur_zeros == 1)

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

    list_abscisse = batage(list_indice_min, list_indice_max)
    list_ordonnée = batage(Y[list_indice_min], Y[list_indice_max])

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


if  __name__=="__main__":
    
    Y= np.array([0, 10, 8, 9, 5, 6.1, 1, 2.1, 1, 5, 4, 4.1, 4, 6, 1])
    X= np.arange(len(Y))

    Min=np.array([0, 2, 4, 6, 8, 10, 12, 14])
    Max=np.array([1, 3, 5, 7, 9, 11, 13])
    

    print("\nListeX",X)
    print("Liste.size", X.size)

    print("\nListeY",Y)
    print("Liste.size", Y.size)

    print("\nMin",Min)
    print("Min.size",Min.size)

    print("\nMax",Max)
    print("Max.size",Max.size)

    plt.figure()
    plt.scatter(X[Min], Y[Min], c='b')
    plt.scatter(X[Max], Y[Max], c='r')
    plt.plot(X, Y)

    plt.figure()
    plt.scatter(X, Y)
    plt.plot(X, Y)
    plt.show()


    X_new, Y_new, _= function_vecteur(Min, Max, X, Y, 0.5)

    Y_new = np.append(Y_new, 0)
    X_new = np.append(X_new, len(X))

    #Affichage des données vu par l'ordinateur
    plt.figure()
    plt.title(f"Point de base: point={Max.size + Min.size}")
    plt.scatter(X[Max], Y[Max], c='b')
    plt.scatter(X[Min], Y[Min], c='r')
    plt.plot(X, Y)

    plt.figure()
    plt.title(f"New point de base: point={X_new.size}")
    plt.scatter( X_new, Y_new)
    plt.plot(X_new, Y_new, c='b')
    plt.plot(X, Y, c='r')

    plt.figure()
    plt.title(f"New point de base: point={X_new.size}")
    plt.scatter( X_new, Y_new)
    plt.plot(X, Y, c='r')

    plt.figure()
    plt.title(f"New point de base: point={X_new.size}")
    plt.scatter( X_new, Y_new)
    plt.plot(X_new, Y_new, c='b')
    plt.show()
