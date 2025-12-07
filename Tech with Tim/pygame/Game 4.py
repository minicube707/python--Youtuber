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
pygame.init()                                   #Initailisation de pygame
win = pygame.display.set_mode((500, 480))       #Création de la fênetre de jeu, (500, 480) taille de la fenetre 
pygame.display.set_caption("Fourth game")        #Titre du jeu

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
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width =  width
        self.height = height
        self.vel = 5
        self.isJumping = False
        self.jumpCount = 10
        self.left =  False
        self.right = False
        self.walkcount = 0

    def draw(self,win):

        #Si la variable walkcount est superieur à 27, la variable walkcount se réinitialise à 0
        if self.walkcount +1 >= 27:
            self.walkcount = 0

        #Si left == True alors l'image afficher au coordonnées (x, y) sera l'élément de la liste walkLeft à walkcount // 3 indice
        if self.left:
            win.blit(walkLeft[self.walkcount // 3], (self.x, self. y))
            self.walkcount +=1

        #Si right == True alors l'image afficher au coordonnées (x, y) sera l'élément de la liste walkRight à walkcount // 3 indice
        elif self.right:
            win.blit(walkRight[self.walkcount // 3], (self.x, self.y))
            self.walkcount +=1

        #Sinon l'image afficher au coordonnées (x, y) sera l'élément debout
        else:
            win.blit(char, (self.x, self.y))



#/////////////////////////////////////////////
#Fonction
#/////////////////////////////////////////////
#Fonction de mise à jour de l'écran
def redrawGameWindow():

    win.blit(bg, (0, 0))
    man.draw(win)
    #Mise à jour de l'écran
    pygame.display.update()   



#/////////////////////////////////////////////
#MainLoop
#/////////////////////////////////////////////
man = Player(300, 400, 64, 64)
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
    if key[pygame.K_LEFT] and man.x > man.vel:

        # La cordonnée X est égale à elle-même moins la vélocité pour chaque itération
        man.x -= man.vel

        #Comme le joueur se déplace à gauche:  left = True right = False
        man.left = True
        man.right = False

    # Si la fleche de droite est appuyé et que le joueur se situe dans une une coordonnée X inférieur à la taille de la fênetre, moins la largueur du joueur,
    # moins la vélocité pour ne pas dépasser de la fênetre
    elif key[pygame.K_RIGHT] and  man.x < 500 - man.width - man.vel:
        # La cordonnée X est égale à elle-même plus la vélocité pour chaque itération
        man.x += man.vel

        #Comme le joueur se déplace à gauche:  left = True right = False
        man.left = False
        man.right = True

    #Si le joueur ne se déplace pas alors right = False left = False et la variable walkcount se réinitialise à 0
    else:
        man.right = False
        man.left = False
        man.walkcount = 0



    #/////////////////////////////////////////////
    #Jump      
    #/////////////////////////////////////////////
    #Si la variable isJump == False et que le joueur presse sur la touche espace alors:
    if not (man.isJumping):
        if key[pygame.K_SPACE]:
            man.isJumping =True
            man.right = False
            man.left = False
            man.walkcount = 0
    
    #Si la variable isJumping == True:
    else:
        if man.jumpCount >= -10:
            #Initialisation
            neg = 1

            #Si le joueur a parcouru la moitié de son saut alors le joueur redescend
            if man.jumpCount < 0: 
                neg = -1

            # L'équation du jump
            man.y -=  (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1

        #Si le jump est terminé, alors la variable isJump == False et le joueur peut sauter à nouveau
        else:
            man.isJumping = False
            man.jumpCount = 10
    
    redrawGameWindow()

#Game over
pygame.quit()
