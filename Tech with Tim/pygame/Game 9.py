import pygame


#/////////////////////////////////////////////
# Initialisation
#/////////////////////////////////////////////
pygame.init()                                   
win = pygame.display.set_mode((500, 480))       
pygame.display.set_caption("Nineth game")        

walkRight = [pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\R1.png'),
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\R2.png'),
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\R3.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\R4.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\R5.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\R6.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\R7.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\R8.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\R9.png')]
                            
walkLeft = [pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\L1.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\L2.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\L3.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\L4.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\L5.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\L6.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\L7.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\L8.png'), 
            pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\L9.png')]

char = pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Character Mouvement\standing.png')

bg = pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Background\Bg.jpg')

bullet_sound = pygame.mixer.Sound("Desktop\Document\Programme\Python\Tech with Tim\pygame\Soudtrack\Bullet.mp3")
hit_sound = pygame.mixer.Sound("Desktop\Document\Programme\Python\Tech with Tim\pygame\Soudtrack\hit.mp3")

music = pygame.mixer.music.load("Desktop\Document\Programme\Python\Tech with Tim\pygame\Music\music.mp3")

clock = pygame.time.Clock()

score = 0

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
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self,win):

        if self.walkcount +1 >= 27:
            self.walkcount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkcount // 3], (self.x, self. y))
                self.walkcount +=1

            elif self.right:
                win.blit(walkRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount +=1

        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):

        self.x = 60
        self.y = 410
        self.walkcount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text =font1.render("-5", 1, (255, 0, 0))
        win.blit(text, (250  - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0

        while i < 100:
            pygame.time.delay(10)
            i += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy (object):
    walkRight = [pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R1E.png'),
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R2E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R3E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R4E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R5E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R6E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R7E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R8E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R9E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R10E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\R11E.png')]
    
    walkLeft = [pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L1E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L2E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L3E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L4E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L5E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L6E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L7E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L8E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L9E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L10E.png'), 
                pygame.image.load('Desktop\Document\Programme\Python\Tech with Tim\pygame\Enemy Mouvement\L11E.png')]
    
    def __init__(self, x, y, width, height, end) -> None:
        self.x = x
        self.y = y
        self.width =  width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkcount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible == True:
            
            if self.walkcount +1 >= 33:
                self.walkcount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkcount // 3], (self.x, self. y))
                self.walkcount +=1

            else:
                win.blit(self.walkLeft[self.walkcount // 3], (self.x, self. y))
                self.walkcount +=1

            #Health Bar
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20,  50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20,  50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 20, self.y, 28, 60)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        
        if self.vel > 0:

            if self.x - self.vel < self.path[1] :
                self.x += self.vel

            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkcount = 0

        else:
            if self.x + self.vel > self.path[0] :
                self.x += self.vel

            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkcount = 0
        
    def hit(self):
        if self.health > 1:
            self.health -= 1
            print("Hit")
        else:
            self.visible = False


#/////////////////////////////////////////////
#Fonction
#/////////////////////////////////////////////
#Fonction de mise à jour de l'écran
def redrawGameWindow():

    win.blit(bg, (0, 0))
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (336, 10))
    man.draw(win)
    goblin.draw(win)

    for bullet in bullets:
        bullet.draw(win)


    pygame.display.update()   


#/////////////////////////////////////////////
#MainLoop
#/////////////////////////////////////////////
    
man = Player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)

shootLoop = 0
bullets = []
run = True

font = pygame.font.SysFont("comicsans", 30, True)

pygame.mixer.music.play(-1)

while run:
    clock.tick(27)

    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0]:

            man.hit()
            score -= 5
                
    if shootLoop > 0:
        shootLoop +=1
    
    if shootLoop  > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #/////////////////////////////////////////////
    #Bullet
    #/////////////////////////////////////////////
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius > goblin.hitbox[0]:
                
                goblin.hit()
                hit_sound.play()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        
        else:
            bullets.pop(bullets.index(bullet))

    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
            bullet_sound.play()
        shootLoop = 1

    #/////////////////////////////////////////////
    #Mouvement DROITE GAUCHE
    #/////////////////////////////////////////////
    if key[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel

        man.left = True
        man.right = False
        man.standing = False

    elif key[pygame.K_RIGHT] and  man.x < 500 - man.width - man.vel:
        man.x += man.vel

        man.left = False
        man.right = True
        man.standing = False

    else:
        man.standing = True 
        man.walkcount = 0

    #/////////////////////////////////////////////
    #Jump      
    #/////////////////////////////////////////////
    if not (man.isJumping):
        if key[pygame.K_UP]:
            man.isJumping =True
            man.right = False
            man.left = False
            man.walkcount = 0
    
    else:
        if man.jumpCount >= -10:
            neg = 1

            if man.jumpCount < 0: 
                neg = -1

            man.y -=  (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1

        else:
            man.isJumping = False
            man.jumpCount = 10
    
    redrawGameWindow()


pygame.quit()
