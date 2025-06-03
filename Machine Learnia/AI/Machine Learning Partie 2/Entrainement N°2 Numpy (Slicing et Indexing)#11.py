import  numpy               as np
import  matplotlib.pyplot   as plt
from    scipy       import misc
from    datetime    import datetime

heure_actuelle = datetime.now().strftime("%H:%M:%S")
print("")
print("L'heure actuelle est :", heure_actuelle)
print("")

A=np.array([[1,2,3],
            [4,5,6],
            [7,8,9]])
print("A=")
print(A)

#Indexing
#Savoir extraire une valeur voulu dans un tableau par des coordonnées 
print("")
print("#Indexing")
print("Première Lingne, Première Cologne =",A[0,0])
print("Dernière Lingne, Dernière Cologne =",A[len(A.shape),len(A.shape)]) # Ou print("Dernière Lingne, Dernière Cologne =",A[2,2])

#Slicing
#Savoir extraire une ou des colonnes/lignes 
print("")
print("#Slicing")
print("Toute la première cologne=",A[:,0])
print("Toute la première linge=",A[0,:])  #Ou print("Toute la première ligne =",A[0])
print("")
print("Toute la dernière cologne=",A[:,len(A.shape)])
print("Toute la dernière linge=",A[len(A.shape),:])
print("")
print("Les lignes des deux premières colognes et des deux première linges =")
print(A[0:2,0:2])
print("Les lignes des deux dernière colognes et des deux dernière linges =")
print(A[-2:,-2:]) #Ou print(A[1:3,1:3]) #Ou print(A[len(A.shape)-1:len(A.shape)+1,len(A.shape)-1:len(A.shape)+1])

#Exercice
print("")
print("Exercice")
print(A[0:3,1:3])


#Subsetting 
#Savoir extraire un tableau à partir d'un tableau
print("")
print("#Subsetting ")
B=A[1:3,1:3]
print("B=")
print(B)

#Ecriture
print("")
print("#Ecriture")
C=A
C[0:2,0:2]=10
print("C=")
print(C)

#Exercice
print("")
print("Exercice")
D=np.zeros((4,4))
print("")
print("D=")
print(D)
D[1:3,1:3]=1
print("")
print("D modifié =")
print(D)

#Pas
print("")
print("#Pas")
E=np.zeros((5,5))
print("E=")
print(E)
E[::2,::2]=1
print("")
print("E modifié =")
print(E)

#Boolean Indexing
#Savoir extraire des données à partir d'un tableau et d'un masque booléan
#On a alors M=Tableau[Masque Booléan / Condition du masque], avec M la Matrice avec les valeurs retenue '=True'
print("")
print("#Boolean Indexing")

F=np.array([['Garder','Retirer','Garder'],
            ['Retirer','Garder','Retirer'],
            ['Garder','Retirer','Garder']])

Masque=np.array([[True,False,True],
                [False,True,False],
                [True,False,True]])
print("F=\n",F)
print("")
print("Masque:\n",Masque)
print("")
print("#Boolean Indexing F[Masque]\n",F[Masque])

F=np.array([[1,2,3],
            [4,5,6],
            [7,8,9]])

print("")
print("F=\n",F)
print("")
print("Affiche la valuer boolean de F, tels que F<5\n",F<5)
print("")
print("Remplace toute les valeur <5 par 10")
G=F.copy()
G[F<5]=10
print(G) 
print("")
H=F[F<5]
print("Liste des nombre inférieur à 5\n",H)
print("La nouvelle shape de H est ",H.shape)

print("")
I=np.random.randint(0,5,[3,3])
print("I=")
print(I)
I=I[Masque]
print("")
print("Application du masque Masque sur I")
print(I)

#Exercice
print("Exercice")
plt.figure()
face=misc.face()
plt.imshow(face)
plt.title("Original:Photo d'un raton laveur en couleur")
plt.show()

plt.figure()
face_gray=misc.face(gray=True)
plt.imshow(face_gray,cmap=plt.cm.gray)
plt.title("Original Gris: Photo d'un raton laveur en monochrome")
plt.show()

print("Original: Le nombre de dimension de la photo en couleur est ",face.shape)
print("Original Gris: Le nombre de dimension de la photo en noir et balnc est ",face_gray.shape)

#Exercice
#Changement de couleur
print("Exercice")
face_gray_copy1=face_gray.copy()
face_gray_copy1[face_gray<85]=0
face_gray_copy1[face_gray>170]=255
face_gray_copy1[(face_gray<=85) & (face_gray>170)]=127
print("Original Tricolor: Le nombre de dimension de la photo en noir, balnc et gris est ",face_gray_copy1.shape)

plt.figure()
plt.imshow(face_gray_copy1,cmap=plt.cm.gray)
plt.title("Original Tricolor: Photo d'un raton laveur en noir, blanc et gris")
plt.show()

#Zoom milieu
face_gray_copy2=face_gray.copy()
face_gray_copy2=face_gray_copy2[256:513,341:683]
print("Zoom: Le nombre de dimension de la photo zoommer est ",face_gray_copy2.shape)
plt.figure()
plt.imshow(face_gray_copy2,cmap=plt.cm.gray)
plt.title("Zoom: Photo zoommer d'un raton laveur en monochrome")
plt.show()

#Corection
h=face_gray_copy2.shape[0]
w=face_gray_copy2.shape[1]
zoom_face=face_gray_copy2[h//4:-h//4,w//4:-w//4]
print("Correction: Le nombre de dimension de la photo zoommer est ",zoom_face.shape)
plt.figure()
plt.imshow(zoom_face,cmap=plt.cm.gray)
plt.title("Correction: Photo zoommer d'un raton laveur en monochrome")
plt.show()

#Bonus 
face_compresion=face[::2,::2]
print("Compression: Le nombre de dimension de la photo zoommer est ",face_compresion.shape)
plt.figure()
plt.imshow(face_compresion)
plt.title("Compression: Photo zoommer d'un raton laveur en couleur")
plt.show()

""""
for i in range(1,11):
    face_compresion=face[::i,::i]
    print("Compression: Le nombre de dimension de la photo zoommer est ",face_compresion.shape," pour un facteur ",i)
    plt.figure()
    plt.imshow(face_compresion)
    plt.title("Compression: Photo zoommer d'un raton laveur en couleur de facteur %i" %i)
plt.show()
"""
