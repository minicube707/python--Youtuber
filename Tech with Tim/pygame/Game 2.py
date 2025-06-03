import pygame

# Info 
#Les coordonnées de l'écran soit (0, 0) en haut à droite, (0, widthScreen) en bas à gauche, (heightScreen, 0) en bas à droite, et (heightScreen, widthScreen) en haut à gauche. 
#Les coordonées du joueur sont celle situé en haut gauche de la forme du joueur

# Initialisation
pygame.init() #Initailisation de pygame
win = pygame.display.set_mode((500, 490))   #Création de la fênetre de jeu
pygame.display.set_caption("Second game")   #Titre du jeu

#Paramétre
x = 50
y = 50
width = 60
height = 50
vel = 10

isJumping = False
jumpCount = 10

#Game
run = True
while run:

    # Fait une pause de 50 millisecondes dans la boucle pour éviter qu'elle ne s'exécute trop rapidement.
    # Cela peut être utilisé pour contrôler la vitesse de la boucle ou pour éviter d'utiliser trop de ressources de l'ordinateur.
    pygame.time.delay(50) 

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

    # Si la fleche de gauche est appuyé et que le joueur se situe sur une coordonnée X supérieur à la vélocité pour ne pas dépasser de la fênetre
    if key[pygame.K_LEFT] and x > vel:
        # La cordonnée X est égale à elle-même moins la vélocité pour chaque itération
        x -= vel

    # Si la fleche de droite est appuyé et que le joueur se situe dans une une coordonnée X inférieur à la taille de la fênetre, moins la largueur du joueur,
    # moins la vélocité pour ne pas dépasser de la fênetre
    if key[pygame.K_RIGHT] and  x < 500 - width - vel:
        # La cordonnée X est égale à elle-même plus la vélocité pour chaque itération
        x += vel

    if not(isJumping):

        # Si la fleche de haut est appuyé et que le joueur se situe sur une coordonnée Y supérieur à la vélocité pour ne pas dépasser de la fênetre
        if key[pygame.K_UP] and y > vel:
            # La cordonnée Y est égale à elle-même moins la vélocité pour chaque itération
            y -= vel

        # Si la fleche de bas est appuyé et que le joueur se situe dans une une coordonnée X inférieur à la taille de la fênetre, moins la largueur du joueur,
        # moins la vélocité pour ne pas dépasser de la fênetre
        if key[pygame.K_DOWN] and  y < 500 - width - vel:
            # La cordonnée Y est égale à elle-même plus la vélocité pour chaque itération
            y += vel

        if key[pygame.K_SPACE]:
            isJumping =True
     #Jump
            
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

        #Si le jump est terminé, alors on sort  de la fonction jump et le joueur peut sauter à nouveau
        else:
            isJumping = False
            jumpCount = 10
    
    #On remplis l'écran de noir, sinon on dessine par dessus l'écran
    win.fill((0, 0, 0)) 

    #Ajout du joueur que l'on rajoute dans l'écran avec (win),
    # la couleur en RGB et ces charactéristique x:position sur l'axe X, y: position sur l'axe Y, width largueur du joueur, height: hauteur du personnage 
    # La forme du joueur est attribué par .rect()
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))  

    #Mise à jour de l'écran
    pygame.display.update()    

#Game over
pygame.quit()