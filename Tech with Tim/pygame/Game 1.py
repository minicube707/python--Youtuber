import pygame

# Info 
#Les coordonnées de l'écran soit (0, 0) en haut à droite, (0, widthScreen) en bas à gauche, (heightScreen, 0) en bas à droite, et (heightScreen, widthScreen) en haut à gauche. 
#Les coordonées du joueur sont celle situé en haut gauche de la forme du joueur

# Initialisation
pygame.init() #Initailisation de pygame
win = pygame.display.set_mode((500, 500))   #Création de la fênetre de jeu
pygame.display.set_caption("Second game")   #Titre du jeu

#Paramétre
x = 50
y = 50
width = 60
height = 40
vel = 10

#Game
run = True
while run:

    # Fait une pause de 100 millisecondes dans la boucle pour éviter qu'elle ne s'exécute trop rapidement.
    # Cela peut être utilisé pour contrôler la vitesse de la boucle ou pour éviter d'utiliser trop de ressources de l'ordinateur.
    pygame.time.delay(100) 

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

    # Si la fleche de gauche est appuyé
    if key[pygame.K_LEFT]:
        # La cordonnée X est égale à elle-même moins la vélocité pour chaque itération
        x -= vel

    # Si la fleche de droite est appuyé
    if key[pygame.K_RIGHT]:
        # La cordonnée X est égale à elle-même plus la vélocité pour chaque itération
        x += vel

    # Si la fleche de haut est appuyé
    if key[pygame.K_UP]:
        # La cordonnée Y est égale à elle-même moins la vélocité pour chaque itération
        y -= vel
    
    # Si la fleche de bas est appuyé
    if key[pygame.K_DOWN]:
        # La cordonnée Y est égale à elle-même plus la vélocité pour chaque itération
        y += vel
    
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