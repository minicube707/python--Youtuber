import pygame, sys
from pathfinder import algorithm

WIDTH, HEIGHT = 1280,736

class Pathfinder:
    def __init__(self, matrix, coord_wall) -> None:

        #setup
        self.matrix = matrix
        self.coord_wall = coord_wall
        self.select_surf = pygame.image.load("Desktop\Document\Programmation\Python\Youtuber\Clear Code\Roomba bot\selection.png").convert_alpha()
        
        #Pathfinding
        self.path = []

        #Roomba
        self.roomba = pygame.sprite.GroupSingle(Roomba(self.empty_path))

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos() #XY
        
        #Coordonnate for the mouse
        row =  mouse_pos[1] // 32
        col =  mouse_pos[0] // 32
        current_cell_value = self.matrix[row][col]

        #Show the mouse only, if the mouse is on the floor
        if current_cell_value == 1:
            rect = pygame.Rect((col * 32,row * 32),(32,32))            
            screen.blit(self.select_surf, rect)

    def create_path(self):

        #Start
        mouse_pos = pygame.mouse.get_pos() #XY
        start_x, start_y = self.roomba.sprite.get_coordonate()
        start = (start_x, start_y)

        #End
        end_x,end_y =  mouse_pos[0] // 32, mouse_pos[1] // 32 

        #Path
        current_cell_value = self.matrix[end_y][end_x]
        if current_cell_value == 1:
            end =  (end_x, end_y)
            self.path = algorithm(len(self.matrix), len(self.matrix[0]), start, end, self.coord_wall)
            self.roomba.sprite.set_path(self.path)

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = (point[0] * 32) + 16
                y = (point[1] * 32) + 16
                points.append((x, y))
                pygame.draw.circle(screen, "blue", (x, y), 2)
            pygame.draw.lines(screen, "blue", False, points, 5)
            
    def update(self):
        self.draw_active_cell()
        self.draw_path()

        #Roomba updating and drawing
        self.roomba.update()
        self.roomba.draw(screen)

    def empty_path(self):
        self.path = []
        
class Roomba(pygame.sprite.Sprite):
    def __init__(self, empty_path) -> None:

        #basic
        super().__init__()
        self.image = pygame.image.load("Desktop\\Document\\Programmation\\Python\\Youtuber\\Clear Code\\Roomba bot\\roomba.png").convert_alpha()
        self.rect = self.image.get_rect(center = (60, 60))

        #mouvement
        self.pos = self.rect.center
        self.speed = 2
        self.direction = pygame.math.Vector2((0, 0))

        #path
        self.path = []
        self.collision_rects = []
        self.empty_path = empty_path
        
    def get_coordonate(self):

        col = self.rect.centerx // 32
        row = self.rect.centery // 32
        return(col, row)
    
    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()
    
    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point[0] * 32) + 16
                y = (point[1] * 32) + 16
                rect = pygame.Rect((x - 2, y - 2), (4, 4))
                self.collision_rects.append(rect)

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        
        else:
            self.direction = pygame.math.Vector2((0, 0))
            self.path = []

    def check_collison(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        
        else:
            self.empty_path()

    def update(self):
        self.pos += self.direction * self.speed
        self.check_collison()
        self.rect.center = self.pos


    
#pygame setup   
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#Game setup
BG = pygame.image.load("Desktop\Document\Programmation\Python\Youtuber\Clear Code\Roomba bot\map.png").convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

#XY / 40x23
matrix = [
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,0,0,0],
	[0,1,1,1,1,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,1,0,0,0],
	[0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0],
	[0,0,0,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0],
	[0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

def get_wall_coordinates(grid):
    wall_coords = set()
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] == 0:
                wall_coords.add((x, y))
    return wall_coords

pathfinder = Pathfinder(matrix, get_wall_coordinates(matrix))

def event():

    #Pygame event
    for event in pygame.event.get():
            
        #Quit pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pathfinder.create_path()

while True:

    event()
    screen.blit(BG, (0, 0))
    pathfinder.update()
    pygame.display.update()
    clock.tick(60)