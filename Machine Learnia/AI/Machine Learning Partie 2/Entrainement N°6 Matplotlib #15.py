import numpy                as np
import matplotlib.pyplot    as plt
from sklearn.datasets       import load_iris
from mpl_toolkits.mplot3d   import Axes3D
from scipy                  import misc

#Affichage de graphique 2D
iris=load_iris()

x = iris.data       #Les datas compris dans la Matrice iris sont enregistrer dans un nouvelle Matrice X
y = iris.target     #Les target/labels compris dans la Matrice iris sont enregistrer dans un nouvelle Matrice y

print("")
print("X=")
print(x)

print("")
print("y=")
print(y)

print("")
print(f'x contient {x.shape[0]} exemples et {x.shape[1]} variables')
print(f'il y a {np.unique(y).size} classes')

#Affichage des deux premières

# 'c' paramètre qui définie la couleur est définie en fonction de la target/label 'y'  
plt.figure()
plt.scatter(x[:,0],x[:,1],c=y) 
plt.title("Graphique d'iris avec les deux première variables")
plt.xlabel("Longueur du sépal")
plt.ylabel("Largeur du sépal")
plt.show()

# 'alpha 'est le paramétre de l'opacité et s est le papramétre de la taille des markers
#'c' est le  paramètre qui désigne la taille des points. Donc ici, la taille des points vaut la valeur de la 3 troisième varaible multiplié par 100
plt.figure()
plt.scatter(x[:,0],x[:,1],c=y,alpha=0.5, s=x[:,2]*100) 
plt.title("Graphique d'iris avec les trois première variables")
plt.xlabel("Longueur du sépal")
plt.ylabel("Largeur du sépal")
plt.show()

#Affichage graphique 3D
ax =plt.axes(projection='3d')
ax.scatter(x[:,0],x[:,1],x[:,2],c=y)
plt.title("Graphique d'iris avec les trois première variables en 3D")
plt.show()

#Affichage graphique 3D  de fonction mathématique

f=lambda x,y : np.sin(x)+np.cos(x+y)

X=np.linspace(0,5,100)
Y=np.linspace(0,5,100)

print("")
print("X",X.shape,"\n",X)

print("")
print("Y:",Y.shape,"\n",Y)

#np.meshgrid(,)
#Elle prend deux tableaux NumPy en entrée (dans votre cas, X et Y) et renvoie deux tableaux NumPy 
#Les deux tableaux Numpy  renvoyés sont de même dimension. Avec le premier dont les valeurs sont alignées horizontalement 
#et le second aligné verticalement 
X_grid, Y_grid =np.meshgrid(X,Y)

print("")
print("X_grid:",X_grid.shape,"\n",X_grid)

print("")
print("Y_grid:",Y_grid.shape,"\n",Y_grid)

Z=f(X_grid, Y_grid)

print("")
print("Les dimensions de Z sont ",Z.shape)

ax =plt.axes(projection='3d')
ax.plot_surface(X_grid, Y_grid ,Z, cmap='plasma')
plt.title("Graphique d'une fonction mathématique")
plt.show()

#Histogramme

# 'bins' est le nombre de section que l'on aura dans notre histogramme 
plt.figure()
plt.hist(x[:,0], bins=20, label='Variable 1')   
plt.hist(x[:,1], bins=20, label='Variable 2')
plt.title("Histogramme de la longueur et largeur du sépal")
plt.xlabel("Longueur et largeur du sépal")
plt.ylabel("Nombre d'iris qui ont cette longueur et largeur de sépal")
plt.show()

#Histogramme d'une image

#plt.axis('off'): Désactivation de la graduation des abscisses et des ordonnées
face=misc.face(gray=True)
plt.figure()
plt.imshow(face, cmap='gray')
plt.title("Raton laveur")
plt.axis('off')
plt.show()

plt.figure()
plt.hist(face.ravel(),bins=255)
plt.title("Distribution des pixels de l'image")
plt.show()

#Histogramme 2D

plt.figure()
plt.hist2d(x[:,0],x[:,1], bins=20, cmap='Blues')
plt.title("Histogramme 2D ")
plt.xlabel("Longueur du sépal")
plt.ylabel("Largeur du sépal")
plt.colorbar()
plt.show()

#Contour plot

#lambada: est utilisée pour créer des fonctions simples et ponctuelles en une seule ligne de code.
#Elle permet aussi de faire le trri d'une liste de tulpe ou de filtrer une liste
#x, y: sont les arguments de la fonction
#np.sin(x)+np.cos(x+y): est l'expression de la fonction
f=lambda x,y : np.sin(x)+np.cos(x+y)

X=np.linspace(0,5,100)
Y=np.linspace(0,5,100)

X_grid, Y_grid =np.meshgrid(X,Y)

Z=f(X_grid,Y_grid)

# '20' est le nombre de niveau dans notre graphique contour plot
plt.figure()
plt.contour(X_grid, Y_grid, Z, 20)  
plt.title("Graphique d'une fonction mathématique avec contour plot")
plt.show()

plt.figure()
plt.contourf(X_grid, Y_grid, Z, 20)  
plt.title("Graphique d'une fonction mathématique en couleur avec contourf plot")
plt.colorbar()
plt.show()

#Imshow()

#Permet d'afficher les Matrice numpy

plt.figure()
plt.title("Graphique de corrélation")
plt.imshow(np.corrcoef(x.T),cmap='Blues')
plt.colorbar()
plt.show()

plt.figure()
plt.title("Image avec X et Y en abssice et ordonnées et Z en couleur")
plt.imshow(Z)
plt.colorbar()
plt.show()

#Bonus
dataset={f"expeérience {i}":np.random.randn( 100) for i in range (3)}

def graphique(data):
    n=len(data)
    plt.figure(figsize=(12,8)) #figsize permet de prendre en paramétre la taille du graphique qu'on veut en inch (pouce)

    for k,i in zip (data.keys(), range(1,n+1)):
        plt.subplot(n,1,i)
        plt.plot(data[k])
        plt.title(k)
    plt.show()

graphique(dataset)



