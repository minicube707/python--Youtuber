import  numpy               as np
import  matplotlib.pyplot   as plt
from    scipy       import misc
from    PIL         import ImageFilter
from    PIL         import Image
from    scipy       import ndimage
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)
os.chdir("../Data")

#Importer une image
Image_Racoon = Image.open("Racoon.png" ) 
Image_Color = Image.open( "Degrader.jpg") 

Image_Color= np.array( Image_Color )
print("")
print("Image_Color")
print( 'classe :', type(Image_Color) )
print( 'type :', Image_Color.dtype )
print( 'taille :', Image_Color.shape )
print( 'modifiable :', Image_Color.flags.writeable )

Image_Racoon= np.asarray( Image_Racoon )
print("")
print("Image_Racoon")
print( 'classe :', type(Image_Racoon) )
print( 'type :', Image_Racoon.dtype )
print( 'taille :', Image_Color.shape )
print( 'modifiable :', Image_Racoon.flags.writeable )

plt.figure()
plt.imshow(Image_Racoon)
plt.title("Image télécharger 1")
plt.axis('off')
plt.show()

plt.figure()
plt.imshow(Image_Color)
plt.title("Image télécharger 2")
plt.axis('off')
plt.show()


#Création d'une image
hauteur = 100
largeur = 300
# mode RGB
canal = 3
new_image_RGB = np.zeros([hauteur, largeur, canal], dtype = np.uint8)
print("")
print("new_image_RGB")
print( 'classe :', type(new_image_RGB) )
print( 'type :', new_image_RGB.dtype )
print( 'taille :', new_image_RGB.shape )
print( 'modifiable :', new_image_RGB.flags.writeable )
plt.figure()
plt.imshow( new_image_RGB )
plt.title("Cadre de l'image")
plt.show()

# rouge : première tranche 0, 100
new_image_RGB[:,:100,:] = (255, 0, 0)
# vert : deuxième tranche 100, 200
new_image_RGB[:,100:200,:] = (0, 255, 0)
# bleu : Troisième tranche 200, 300
new_image_RGB[:,200:,:] = (0, 0, 255)
plt.figure()
plt.imshow(new_image_RGB)
plt.title("Génération d'image")
plt.show()
"""
"""
#Création d'une image unie aléatoire
hauteur = 100
largeur = 300
# mode RGB
canal = 3
Image_unie = np.zeros([hauteur, largeur, canal], dtype = np.uint8)
print("")
print("Image_unie")
print( 'classe :', type(Image_unie) )
print( 'type :', Image_unie.dtype )
print( 'taille :', Image_unie.shape )
print( 'modifiable :', Image_unie.flags.writeable )

for i in range( 1,4):
    Image_unie[:,:,:] = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
    plt.figure()
    plt.imshow(Image_unie)
    plt.title("Génération d'image unie numéro %i " %i)
    plt.axis('off')
    plt.show()

"""
"""
#Création d'une image bruit RGB
hauteur = 100
largeur = 100
# mode RGB
canal = 3
Image_bruit_RGB = np.random.randint(0, 255, size=(hauteur, largeur, 3), dtype=np.uint8)
print("")
print("Image_bruit")
print( 'classe :', type(Image_bruit_RGB) )
print( 'type :', Image_bruit_RGB.dtype )
print( 'taille :', Image_bruit_RGB.shape )
print( 'modifiable :', Image_bruit_RGB.flags.writeable )

for i in range( 1,4):
    Image_bruit_RGB = np.random.randint(0, 255, size=(hauteur, largeur, 3), dtype=np.uint8)
    plt.figure()
    plt.imshow(Image_bruit_RGB)
    plt.title("Génération d'image bruit Gris numéro %i " %i)
    plt.axis('off')
    plt.show()


#Création d'une image bruit Gris
hauteur = 100
largeur = 100
Image_bruit_Grey = np.zeros([hauteur, largeur], dtype = np.uint8)
print("")
print("Image_bruit")
print( 'classe :', type(Image_bruit_Grey) )
print( 'type :', Image_bruit_Grey.dtype )
print( 'taille :', Image_bruit_Grey.shape )
print( 'modifiable :', Image_bruit_Grey.flags.writeable )

for i in range( 1,4):
    Image_bruit_Grey = np.random.randint(0, 255, size=(hauteur, largeur), dtype=np.uint8)
    plt.figure()
    plt.imshow(Image_bruit_Grey, cmap='gray')
    plt.title("Génération d'image bruit RGB numéro %i " %i)
    plt.axis('off')
    plt.show()


 
face=misc.face()
print('taille de face:', face.shape)
plt.figure()
plt.imshow(face)
plt.title("Original: Photo d'un raton laveur en couleur")
plt.axis('off')
plt.show()

#Enregistrer une image
PIL_image = Image.fromarray( np.uint8(face) )
PIL_image
#PIL_image.save("Desktop\Document\Programme\Python\AI\Data\Racoon.jpg") ou #PIL_image.save("Desktop\Document\Programme\Python\AI\Data\Racoon.png")


plt.figure()
face_gray=misc.face(gray=True)
plt.imshow(face_gray,cmap=plt.cm.gray)
plt.title("Original Gris: Photo d'un raton laveur en noir et blanc")

print("Original: Le nombre de dimension de la photo en couleur est ",face.shape)
print("Original Gris: Le nombre de dimension de la photo en noir et balnc est ",face_gray.shape)


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

#Zoom milieu
face_gray_copy2=face_gray.copy()
face_gray_copy2=face_gray_copy2[256:513,341:683]
print("Zoom: Le nombre de dimension de la photo zoommer est ",face_gray_copy2.shape)
plt.figure()
plt.imshow(face_gray_copy2,cmap=plt.cm.gray)
plt.title("Zoom: Photo zoommer d'un raton laveur en noir, blanc et gris")
plt.show()

#Corection
h=face_gray_copy2.shape[0]
w=face_gray_copy2.shape[1]
zoom_face=face_gray_copy2[h//4:-h//4,w//4:-w//4]
print("Correction: Le nombre de dimension de la photo zoommer est ",zoom_face.shape)
plt.figure()
plt.imshow(zoom_face,cmap=plt.cm.gray)
plt.title("Correction: Photo zoommer d'un raton laveur en noir, blanc et gris")
plt.show()

#Bonus 
face_compresion=face[::2,::2]
print("Compression: Le nombre de dimension de la photo zoommer est ",face_compresion.shape)
plt.figure()
plt.imshow(face_compresion)
plt.title("Compression: Photo zoommer d'un raton laveur en couleur")
plt.show()


for i in range(1,11):
    face_compresion=face[::i,::i]
    print("Compression: Le nombre de dimension de la photo zoommer est ",face_compresion.shape," pour un facteur ",i)
    plt.figure()
    plt.imshow(face_compresion)
    plt.title("Compression: Photo zoommer d'un raton laveur en couleur de facteur %i" %i)
plt.show()


#Inversion des couleurs
face_inver =face.copy()
face_inver = 255 - face_inver

plt.figure()
plt.imshow(face_inver)
plt.title("Inversion: Photo zoommer d'un raton laveur en couleur")
plt.axis('off')
plt.show()

#Image Monocromatique

Image_Color_R = Image_Color.copy()
Image_Color_R[:,:,(1,2)] = 0
plt.figure()
plt.imshow(Image_Color_R)
plt.title("Monochromatique Rouge")

Image_Color_B = Image_Color.copy()
Image_Color_B[:,:,(0,1)] = 0
plt.figure()
plt.imshow(Image_Color_B)
plt.title("Monochromatique Bleu")

Image_Color_V = Image_Color.copy()
Image_Color_V[:,:,(2,2)] = 0
plt.figure()
plt.imshow(Image_Color_V)
plt.title("Monochromatique Vert")
plt.show()

#Concaténation

Image_Color_RGB = np.concatenate((Image_Color,Image_Color_R, Image_Color_V, Image_Color_B))
plt.figure()
plt.imshow(Image_Color_RGB)
plt.title("Concaténation: Photo zoommer d'un raton laveur en couleur")
plt.show()


#Histogramme des pixels
plt.figure()
plt.hist(face.flatten(), bins = 20, density = True , alpha = .5 , edgecolor = 'black', color = 'red')
plt.title("Compossition des pixels de l'image ")
plt.ylabel("Quantité des pixels")
plt.show()


#Ajout d'un filtre
face_copy=face.copy()
img = Image.fromarray( np.uint8( face_copy ) )
img_BLUR = img.filter( ImageFilter.BLUR )
# Convertir l'image en tableau numpy
img_blur_array = np.array(img_BLUR)
# Afficher l'image avec plt
plt.imshow(img_blur_array)
plt.title("Image Origianl avec un filtre flou")
plt.axis('off')
plt.show()

plt.hist(face_copy.flatten(), bins=20, density=True , alpha=.5 , edgecolor='black', color='red' , label = 'Image originale')
plt.hist( np.array(img_BLUR).flatten(), bins=20, density=True , alpha=.3 , edgecolor='black', color='blue', label = 'Filtre BLUR')
plt.title("Compossition des pixels de l'image ")
plt.legend()
plt.show()

#CONTOUR 
face_copy=face.copy()
img_CONTOUR = img.filter( ImageFilter.CONTOUR )
# Convertir l'image en tableau numpy
img_contour_array = np.array(img_CONTOUR)
# Afficher l'image avec plt
plt.imshow(img_contour_array)
plt.title("Image Origianl avec un filtre qui affiche les contour")
plt.axis('off')
plt.show()

plt.hist(face_copy.flatten(), bins=20, density=True , alpha=.5 , edgecolor='black', color='red' , label = 'Image originale')
plt.hist(np.array(img_CONTOUR).flatten(), bins=20, density=True , alpha=.3 , edgecolor='black', color='blue', label = 'Filtre CONTOUR')
plt.title("Compossition des pixels de l'image ")
plt.legend()
plt.show()

#Création d'un échéquier

echiquier_array = np.zeros([200, 200], dtype = np.uint8)
for x in range(200):
    for y in range(200):
        if (x % 50) // 25 == (y % 50) // 25:
            echiquier_array[x, y] = 0
        else:
            echiquier_array[x, y] = 255
#Contour
echiquier_array[0:1,:]=0
echiquier_array[:,0:1]=0
echiquier_array[:,-1:]=0
echiquier_array[-1:,:]=0
#Affichage
plt.imshow(echiquier_array, cmap='Greys_r')
plt.title("Echecier")
plt.axis('off')
plt.show()

#Reduction des couleurs de l'image

face_32 = face_copy // 32 * 32
face_128 = face_copy // 128 * 128
#Affichage
face_compil= np.concatenate((face_copy, face_32, face_128), axis=1)
plt.imshow(face_compil)
plt.title("Compil de reduction de couleur")
plt.axis('off')
plt.show()

#Correction Gamma

face_1_22 = 255.0 * (face_copy / 255.0)**(1 / 2)
face_22 = 255.0 * (face_copy / 255.0)**2
#Affichage
face_gamma = np.concatenate((face_1_22, face_copy, face_22), axis=1)
pil_img = Image.fromarray(np.uint8(face_gamma))
plt.imshow(pil_img)
plt.title("Compil de correction gamma")
plt.axis('off')
plt.show()


face_exp=face.copy()

rotated_img = ndimage.rotate(face_exp,90)
plt.figure()
plt.imshow(rotated_img)
plt.title("Photo tournée de 90°")
plt.axis('off')
rotated_img = ndimage.rotate(face_exp,180)
plt.figure()
plt.imshow(rotated_img)
plt.title("Photo tournée de 180°")
plt.axis('off')
rotated_img = ndimage.rotate(face_exp,270)
plt.figure()
plt.imshow(rotated_img)
plt.title("Photo tournée de 270°")
plt.axis('off')
plt.show()