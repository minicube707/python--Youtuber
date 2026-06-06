import pygame
import math

from utils import scale_image, blit_rotate_center

pygame.init()

GRASS = scale_image(pygame.image.load("../imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("../imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("../imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("../imgs/finish.png")
FINISH_POSITION = (130, 250)
FINISH_MASK = pygame.mask.from_surface(FINISH)

RED_CAR = scale_image(pygame.image.load("../imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("../imgs/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

class AbstractCar:    
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
    
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        self.y -= vertical
        self.x -= horizontal
    
    def reset(self):
        self.angle = 0
        self.x, self.y = self.START_POS
    
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offest = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offest)
        return poi
       
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
        
    def bounce(self):
        self.vel = -self.vel
        self.move()

class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)
    
    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel) 
        self.path = path
        self.current_path = 0
        self.vel = max_vel
        
    def draw_point(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)
    
    def draw(self, win):
        super().draw(win)
        #self.draw_point(win)
    
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_path]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        
        if y_diff == 0:
            desired_randian_angle = math.pi / 2
        else:
            desired_randian_angle = math.atan(x_diff / y_diff)
        
        if target_y > self.y:
            desired_randian_angle += math.pi
        
        difference_in_angle = self.angle - math.degrees(desired_randian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360
        
        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
    
    def update_path_point(self):
        
        target =self.path[self.current_path]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        
        if rect.collidepoint(*target):
            self.current_path += 1

    def move(self):
        if self.current_path >= len(self.path):
            return
        
        self.calculate_angle()
        self.update_path_point()
        super().move()
    
    def reset(self):
        self.current_path = 0
        super().reset()
        
def draw(win, images, player_car, computer_car):
    
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()

def move_player(player_car):
    
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_e]:
        player_car.rotate(right=True)
        
    if keys[pygame.K_z]:
        player_car.move_forward()
        moved = True
    if keys[pygame.K_s]:
        player_car.move_backward()
        moved = True
        
    if not moved:
        player_car.reduce_speed()

def handle_collision(player_car, computer_car):

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()
    
    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        player_car.reset()
        computer_car.reset()
        
    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            computer_car.reset()

images = [
    (GRASS, (0, 0)),
    (TRACK, (0, 0)),
    (FINISH, FINISH_POSITION),
    (TRACK_BORDER, (0, 0))
]

path = [
    (168, 144),
    (124, 71),
    (59, 121),
    (55, 457),
    (311, 719),
    (391, 712),
    (405, 538),
    (495, 474),
    (599, 534),
    (607, 698),
    (678, 735),
    (740, 663),
    (735, 385),
    (438, 364), 
    (391, 319),
    (452, 266),
    (687, 262),
    (737, 217),
    (736, 111),
    (683, 71),
    (345, 69),
    (274, 118),
    (279, 356),
    (227, 412),
    (166, 360), 
    (179, 254)
]

FPS = 60
run = True
clock = pygame.time.Clock()
player_car = PlayerCar(4, 4)
computer_car = ComputerCar(4, 4, path)

while run:
    
    clock.tick(FPS)
    
    draw(WIN, images, player_car, computer_car)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
            break
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     computer_car.path.append(pos)
            
    move_player(player_car)
    computer_car.move()
    
    handle_collision(player_car, computer_car)

#print(computer_car.path)      
pygame.quit()
            