import numpy                as np
import matplotlib.pyplot    as plt
from scipy.interpolate  import interp1d
from scipy              import optimize
from scipy              import signal   
from scipy              import fftpack
from scipy              import ndimage


#Interpolagion linéaire
#interp1d permet de rajouter des donnnées à partir des données initiales
x= np.linspace(0,10,10)
y=x**2
plt.figure()
plt.title("Model initial linéaire")
plt.scatter(x,y)
plt.scatter(x,y,label="Model initial")
plt.xlabel("X")
plt.ylabel("f(x)=y")
plt.legend()
plt.show()

f=interp1d(x,y, kind='linear')  #interp1d récupère les données ainsi que le type de model à rendre
new_x=np.linspace(0,10,30)      #Nouvelle variable avec le nombre de donnée à générer   
result=f(new_x)                 #Création de la relation entre les données générer (x) et le model 

plt.figure()
plt.title("Model prolongé linéaire")
plt.scatter(x,y,label="Model initial")
plt.scatter(new_x,result,c='r',label="Model prolongé par interpolation")
plt.xlabel("X")
plt.ylabel("f(x)=y")
plt.legend()
plt.show()

#Interpolagion cubic
x= np.linspace(0,10,10)
y=np.sin(x)
plt.figure()
plt.title("Model initial cubic")
plt.scatter(x,y)
plt.scatter(x,y,label="Model initial")
plt.xlabel("X")
plt.ylabel("f(x)=y")
plt.legend()
plt.show()

f=interp1d(x,y, kind='cubic')
new_x=np.linspace(0,10,30)
result=f(new_x)

plt.figure()
plt.title("Model prolongé")
plt.scatter(x,y,label="Model initial cubic")
plt.scatter(new_x,result,c='r',label="Model prolongé par interpolation")
plt.xlabel("X")
plt.ylabel("f(x)=y")
plt.legend()
plt.show()

#Optimisation
#De préférenece à faire sur scikit learn
#Permet de transfomer un nuage de points en une fonction mathématique linéaire

x= np.linspace(0,2,100)
y= 1/3*x**3-3/5*x**2+2+np.random.randn(x.shape[0])/20
plt.figure()
plt.title("Model initial optimisation")
plt.scatter(x,y,label="data")
plt.xlabel("X")
plt.ylabel("f(x)=y")
plt.legend()
plt.show()

def f(x,a,b,c,d):
    return a*x**3+b*x**2+c*x+d

result1,result2=optimize.curve_fit(f,x,y)
print("")
print("#Optimisation")
print("result1=",result1)   #result1 est une matrice avec les différents paramétres de notre model a,b,c,d de la fonction f 
print("result2=",result2)   #result2 est une matrice avec les covariences des paramétres

plt.figure()
plt.title("Model final optimisation")
plt.scatter(x,y,label="data")
plt.scatter(x,f(x,result1[0],result1[1],result1[2],result1[3]), c='g',label="fonction d'optimisation")
plt.xlabel("X")
plt.ylabel("f(x)=y")
plt.legend()
plt.show()

#Minimize
#Permet de trouver le minimun local d'un fonction linéaire

def f(x):
    return x**2+15*np.sin(x)

x=np.linspace(-10,10,100)
plt.figure()
plt.title("Model initial minimisation")
plt.plot(x,f(x),label="Courbe de la fonction")
plt.xlabel("X")
plt.ylabel("f(x)=y")
plt.legend()
plt.show()

print("")
print("#Minimize")

print("")
print("Résultat de la fonction")
x0=1
print(optimize.minimize(f,x0))
min=optimize.minimize(f,x0).x #Le .x permet d'accéder aux valeurs de x
plt.figure()

plt.title("Model initial minimisation")
plt.plot(x,f(x),label="Courbe de la fonction")
plt.scatter(min,f(min),label="Minimun local",c='b',marker='+')
plt.scatter(x0,f(x0),label="Point de départ", c='r')
plt.xlabel("X")
plt.ylabel("f(x)=y")
plt.legend()
plt.show()

def f(x):
    return np.sin(x[0]) +np.cos(x[0]+x[1])*np.cos(x[0])

X=np.linspace(-3,3,100)
Y=np.linspace(-3,3,100)

X,Y =np.meshgrid(X,Y)
plt.figure()
plt.contourf(X,Y,f(np.array([X,Y])), 20)
plt.title("Fonction mathématique")
plt.colorbar()
plt.show()

x0=np.zeros((2))

print("")
print("X0=",x0)

print("")
print(optimize.minimize(f,x0=x0))
min=optimize.minimize(f,x0=x0).x

print("")
print("min=",min)

plt.figure()
plt.contourf(X,Y,f(np.array([X,Y])), 20)
plt.scatter(x0[0],x0[1], marker='+', c='r', s=100,label="Point de départ")
plt.scatter(min[0],min[1], c='g', s=100,label="Minimun local")
plt.title("Fonction mathématique avec minimum local")
plt.colorbar()
plt.legend()
plt.show()

#Tratement du signal
#signal.detrend() Supprimez la tendance linéaire le long de l’axe des données.

x=np.linspace(0,20,100)
y=x + 4*np.sin(x)+np.random.randn(X.shape[0])
plt.figure()
plt.plot(x,y)
plt.title("Signal")
plt.show()

new_y=signal.detrend(y)
plt.figure()
plt.plot(x,new_y, label="Nouveau signal")
plt.plot(x,y, label="Signal initial")
plt.title("Nouveau Signal")
plt.legend()
plt.show()


#Transformation de fourrier

x=np.linspace(0,30,1000)
y= 3*np.sin(x)+2*np.sin(5*x)+np.sin(10*x)
plt.figure()
plt.plot(x,y)
plt.title("Signal")
plt.show()


fourier = fftpack.fft(y)
#Permet de décomposer un signal péréodique en ses composantes de fréquence.
#Cela signifie qu'elle convertit un signal du domaine temporel (amplitude en fonction du temps)
#en un domaine de fréquence (amplitude en fonction de la fréquence).

#Après avoir exécuté cette ligne, la variable fourier contiendra les coefficients de la transformée de Fourier discrète du signal y.
#Ces coefficients représentent l'amplitude et la phase des différentes fréquences présentes dans le signal y.
#fourier sera également un tableau NumPy.
 

frequnece= fftpack.fftfreq(y.size)
#Cette fonction génère un tableau NumPy contenant les fréquences correspondant à la transformée de Fourier discrète (FFT) de votre signal. Les fréquences sont en unités d'oscillations par échantillon.
#L'indice 0 du tableau correspond à la fréquence nulle (DC),
#et les fréquences positives sont suivies des fréquences négatives.

plt.figure()
plt.plot(np.abs(frequnece),np.abs(fourier))
plt.title("Extraction des fréquences du signal")
plt.show()

#Transformation de fourrier traitement de signal

x= np.linspace(0,30,1000)
y= 3*np.sin(x)+2*np.sin(5*x)+np.sin(10*x) + np.random.random(x.shape[0])*10

plt.figure()
plt.plot(x,y)
plt.title("Signal abimé")
plt.show()

fourier = fftpack.fft(y)
frequnece= fftpack.fftfreq(y.size)
plt.figure()
abs_fourier=np.abs(fourier)
abs_frequence=np.abs(frequnece)
plt.plot(abs_frequence,abs_fourier)
plt.title("Frequnece analyser")
plt.show()

fourier[abs_fourier<400]=0

plt.figure()
plt.plot(np.abs(frequnece),np.abs(fourier))
plt.title("Frequence traité")
plt.show()

filtered_signal=fftpack.ifft(fourier)#Permet de faire l'inverse de la transfomation de fourier

plt.figure()
plt.plot(x,y, lw=0.5)
plt.plot(x,filtered_signal, lw=3, alpha=0.7)
plt.title("Signal traité et remis en forme comparé au signal initial")
plt.show()

# Traitement de l'image

np.random.seed(0)
X=np.zeros((32,32))
X[10:-10,10:-10]=1
X[np.random.randint(0,32,30),np.random.randint(0,32,30)]=1
plt.figure()
plt.title("Image")
plt.imshow(X)
plt.show()

open_x_1=ndimage.binary_opening(X)
plt.figure()
plt.imshow(open_x_1)
plt.title("Image traité opening")
plt.show()

open_x_2=ndimage.binary_erosion(X)
plt.figure()
plt.imshow(open_x_2)
plt.title("Image traité erosion")
plt.show()

open_x_3=ndimage.binary_dilation(X)
plt.figure()
plt.imshow(open_x_3)
plt.title("Image traité dilation")
plt.show()

open_x_4=ndimage.binary_propagation(X)
plt.figure()
plt.imshow(open_x_4)
plt.title("Image traité propagation")
plt.show()

open_compil= np.concatenate((X,open_x_1,open_x_2,open_x_3,open_x_4), axis=1)
plt.imshow(open_compil)
plt.title("Compil de des différence transformation")
plt.show()

# Analyse d'une image

image_bacteria=plt.imread('Desktop\Document\Programme\Python\AI\Data\Bactéria.png')
image_bacteria=image_bacteria[:,:,0]
plt.figure()
plt.imshow(image_bacteria, cmap=plt.cm.gray)
plt.title("Image de bactérie")

plt.show()

print("")
print("Les dimension de l'image de sont ", image_bacteria.shape)

image_2=np.copy(image_bacteria)
plt.figure()
plt.hist(image_2.ravel(),bins=255)
plt.title("Histogramme de l'image de bactérie")
plt.show()

image_masque=image_bacteria<0.6
print("")
print("Le masque ressemble à ")
print(image_masque)

plt.figure()
plt.imshow(image_masque)
plt.title("Affichage du masque")
plt.show()

open_bacteria=ndimage.binary_opening(image_masque)
plt.figure()
plt.imshow(open_bacteria)
plt.title("Image traité de la bactérie")
plt.show()

label_image,n_label=ndimage.label(open_bacteria)
print("")
print("Il y a ",n_label," différente(s) zone(s)")
plt.figure()
plt.imshow(label_image)
plt.title("Image traité affichant les différentes zones")
plt.show()

sizes=ndimage.sum(open_bacteria, label_image,range(n_label))
#Permet de compter tout les pixels qui sont affilié à une étiquette
#open_bacteria=image original
#label_image= image avec les étiquettes
#range(n_label)=le nombre d'étiquette

print("")
print("Les données sont ")
print(sizes)
plt.figure()
plt.scatter(range(n_label), sizes, c='orange')
plt.title("Graphique affichant la taille des bactéries")
plt.show()
