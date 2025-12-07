import pygame
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)


#/////////////////////////////////////////////
# Info 
#/////////////////////////////////////////////
#Les coordonnées de l'écran soit (0, 0) en haut à droite, (0, widthScreen) en bas à gauche, (heightScreen, 0) en bas à droite, et (heightScreen, widthScreen) en haut à gauche. 
#Les coordonées du joueur sont celle situé en haut gauche de la forme du joueur



#/////////////////////////////////////////////
# Initialisation
#/////////////////////////////////////////////
pygame.init() #Initailisation de pygame
win = pygame.display.set_mode((500, 480))   #Création de la fênetre de jeu, (500, 480) taille de la fenetre 
pygame.display.set_caption("Third game")   #Titre du jeu

#Création des liste contenant les images pour les animations de mouvement du personnage
walkRight = [pygame.image.load('Character Mouvement\R1.png'),
            pygame.image.load('Character Mouvement\R2.png'),
            pygame.image.load('Character Mouvement\R3.png'), 
            pygame.image.load('Character Mouvement\R4.png'), 
            pygame.image.load('Character Mouvement\R5.png'), 
            pygame.image.load('Character Mouvement\R6.png'), 
            pygame.image.load('Character Mouvement\R7.png'), 
            pygame.image.load('Character Mouvement\R8.png'), 
            pygame.image.load('Character Mouvement\R9.png')]
                            
walkLeft = [pygame.image.load('Character Mouvement\L1.png'), 
            pygame.image.load('Character Mouvement\L2.png'), 
            pygame.image.load('Character Mouvement\L3.png'), 
            pygame.image.load('Character Mouvement\L4.png'), 
            pygame.image.load('Character Mouvement\L5.png'), 
            pygame.image.load('Character Mouvement\L6.png'), 
            pygame.image.load('Character Mouvement\L7.png'), 
            pygame.image.load('Character Mouvement\L8.png'), 
            pygame.image.load('Character Mouvement\L9.png')]

#Personnage imobile
char = pygame.image.load('Character Mouvement\standing.png')

#Arrière Plan
bg = pygame.image.load('Background\Bg.jpg')

clock = pygame.time.Clock()



#/////////////////////////////////////////////
#Paramétre
#/////////////////////////////////////////////
#Position du joueur
x = 50
y = 400

#Forme du joueur
width = 64
height = 64

#Vistesse de déplacement du joueur
vel = 5

#Est ce que le joueur saute
isJumping = False
jumpCount = 10

#Est ce que le joueur va à droite ou à gauche
left =  False
right = False

walkcount = 0



#/////////////////////////////////////////////
#Fonction
#/////////////////////////////////////////////
#Fonction de mise à jour de l'écran
def redrawGameWindow():
    global walkcount

    #Afficher l'arrière plan au coordonnées (0, 0)
    win.blit(bg, (0, 0))
    
    #Si la variable walkcount est superieur à 27, la variable walkcount se réinitialise à 0
    if walkcount +1 >= 27:
        walkcount = 0

    #Si left == True alors l'image afficher au coordonnées (x, y) sera l'élément de la liste walkLeft à walkcount // 3 indice
    if left:
        win.blit(walkLeft[walkcount // 3], (x, y))
        walkcount +=1

    #Si right == True alors l'image afficher au coordonnées (x, y) sera l'élément de la liste walkRight à walkcount // 3 indice
    elif right:
        win.blit(walkRight[walkcount // 3], (x, y))
        walkcount +=1
    
    #Sinon l'image afficher au coordonnées (x, y) sera l'élément debout
    else:
        win.blit(char, (x, y))
    
    #Mise à jour de l'écran
    pygame.display.update()   



#/////////////////////////////////////////////
#MainLoop
#/////////////////////////////////////////////
run = True
while run:

    
    clock.tick(27)

    # Parcourt tous les événements pygame qui se sont produits depuis la dernière itération de la boucle.
    # Les événements sont des actions générées par l'utilisateur, telles que des clics de souris, des pressions de touches, etc.
    for event in pygame.event.get():

        # Vérifie si l'événement est de type "QUIT", ce qui signifie généralement que l'utilisateur a demandé à fermer la fenêtre de l'application 
        # (par exemple, en cliquant sur le bouton de fermeture de la fenêtre).
        if event.type == pygame.QUIT:

            #  Si l'événement de fermeture de la fenêtre est détecté, cela modifie la valeur de run à False,
            # ce qui entraîne la sortie de la boucle principale (while run:), et donc la fin du programme.
            run = False

    # List des touches du clavier
    key = pygame.key.get_pressed()



    #/////////////////////////////////////////////
    #Mouvement DROITE GAUCHE
    #/////////////////////////////////////////////
    # Si la fleche de gauche est appuyé et que le joueur se situe sur une coordonnée X supérieur à la vélocité pour ne pas dépasser de la fênetre
    if key[pygame.K_LEFT] and x > vel:

        # La cordonnée X est égale à elle-même moins la vélocité pour chaque itération
        x -= vel

        #Comme le joueur se déplace à gauche:  left = True right = False
        left = True
        right = False

    # Si la fleche de droite est appuyé et que le joueur se situe dans une une coordonnée X inférieur à la taille de la fênetre, moins la largueur du joueur,
    # moins la vélocité pour ne pas dépasser de la fênetre
    elif key[pygame.K_RIGHT] and  x < 500 - width - vel:
        # La cordonnée X est égale à elle-même plus la vélocité pour chaque itération
        x += vel

        #Comme le joueur se déplace à gauche:  left = True right = False
        left = False
        right = True

    #Si le joueur ne se déplace pas alors right = False left = False et la variable walkcount se réinitialise à 0
    else:
        right = False
        left = False
        walkcount = 0



    #/////////////////////////////////////////////
    #Jump      
    #/////////////////////////////////////////////
    #Si la variable isJump == False et que le joueur presse sur la touche espace alors:
    if not (isJumping):
        if key[pygame.K_SPACE]:
            isJumping =True
            right = False
            left = False
            walkcount = 0
    
    #Si la variable isJumping == True:
    else:
        if jumpCount >= -10:
            #Initialisation
            neg = 1

            #Si le joueur a parcouru la moitié de son saut alors le joueur redescend
            if jumpCount < 0: 
                neg = -1

            # L'équation du jump
            y -=  (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1

        #Si le jump est terminé, alors la variable isJump == False et le joueur peut sauter à nouveau
        else:
            isJumping = False
            jumpCount = 10
    
    redrawGameWindow()

#Game over
pygame.quit()
