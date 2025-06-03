import pygame
import  random
import math

pygame.init()

Black = (0, 0, 0)
Withe = (255, 255, 255)
Green = (0, 255, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 10
GRID_WIDTH =  WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

def gen(number):
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(number)])

def draw_grid():

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, Withe, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for column  in range(GRID_WIDTH):
        pygame.draw.line(screen, Withe, (column * TILE_SIZE, 0), (column * TILE_SIZE, HEIGHT))

#Drawing
def draw_grid_Grass(positions):

    for position in positions:
        column, row = position
        top_left = (column * TILE_SIZE, row *  TILE_SIZE)
        pygame.draw.rect(screen, Green, (*top_left, TILE_SIZE, TILE_SIZE))

def draw_grid_Sheep(positions):
    
    for position in positions:
        column, row = position
        top_left = (column * TILE_SIZE, row *  TILE_SIZE)
        pygame.draw.rect(screen, Withe, (*top_left, TILE_SIZE, TILE_SIZE))

#Update position
def adjust_grid_Grass(positions_Grass):

    all_neighbors = set()
    new_positions = set()

    #Vérifie si l'individue n'est pas isolé, s'il est il meurt
    for position in positions_Grass:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions_Grass, neighbors))

        """if len(neighbors) > 2:
            new_positions.add(position)"""

    #Vérifie si l'on peut propager l'herbe
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions_Grass, neighbors))

        if  len(neighbors) > 2:
            new_positions.add(position)

    return new_positions

def adjust_grid_Sheep(position_Grass, positions_Sheep):

    new_positions_Sheep = set()
    reproduction_Sheep = set()

    for Sheep_pos in positions_Sheep:
        neighbors = get_neighbors(Sheep_pos)
        reproduction = False

        #Si le mouton est tout seul, il meurt d'isolement et si le mouton est entouré de moton il meurt de surpopulation
        neighbors = list(filter(lambda x: x in position_Grass, neighbors))
        if len(neighbors) <= 2 or len(neighbors)  >= 6:
            continue

        #Reproduction
        for element in neighbors:
            if element in position_Grass:
                reproduction_Sheep.add(element)
                position_Grass.remove(element)
                reproduction = True
                continue

        #Searching for food
        if reproduction == False and len(position_Grass) != 0:
            smalest_distance = 1_000
            smalest_x = 1


            for Grass_pos in position_Grass:

                X = Grass_pos[0] - Sheep_pos[0]
                Y = Grass_pos[1] - Sheep_pos[1]
                distance = math.sqrt(X**2 + Y**2)

                if distance < smalest_distance:
                    smalest_distance = distance
                    smalest_x = X
            
            #Si le mouton est trop loin de la nourriture il meurt 
            if smalest_distance == 0 or smalest_distance > 10:
                continue

            theta = math.acos( smalest_x / smalest_distance )
            
            if Y > 0:

                if theta < 19/50:
                    new_positions_Sheep.add((Sheep_pos[0]+1, Sheep_pos[1]))

                elif theta < 117/100 and theta > 19/50:
                    new_positions_Sheep.add((Sheep_pos[0]+1, Sheep_pos[1]+1))

                elif theta < 39/20 and theta > 117/100:
                    new_positions_Sheep.add((Sheep_pos[0], Sheep_pos[1]+1))

                elif theta < 137/50 and theta > 39/20:
                    new_positions_Sheep.add((Sheep_pos[0], Sheep_pos[1]+1))

                elif theta < math.pi:
                    new_positions_Sheep.add((Sheep_pos[0]-1, Sheep_pos[1]))

            else:

                if theta < 19/50:
                    new_positions_Sheep.add((Sheep_pos[0]+1, Sheep_pos[1]))

                elif theta < 117/100 and theta > 19/50:
                    new_positions_Sheep.add((Sheep_pos[0]+1, Sheep_pos[1]-1))

                elif theta < 39/20 and theta > 117/100:
                    new_positions_Sheep.add((Sheep_pos[0], Sheep_pos[1]-1))

                elif theta < 137/50 and theta > 39/20:
                    new_positions_Sheep.add((Sheep_pos[0], Sheep_pos[1]-1))

                elif theta < math.pi:
                    new_positions_Sheep.add((Sheep_pos[0]-1, Sheep_pos[1]))

    new_positions_Sheep.update(reproduction_Sheep)           
    return position_Grass, new_positions_Sheep


def get_neighbors(pos):
    x, y = pos
    neightbors = []

    for dx in [-1, 0, 1]: 

        if x + dx < 0 or x + dx >  GRID_WIDTH:
            continue

        for dy in [-1, 0, 1]:

            if y + dy < 0 or y + dy >  GRID_HEIGHT:
                continue

            if dx == 0 and dy == 0:
                continue

            neightbors.append((x + dx, y + dy))

    return neightbors

def main():

    running = True
    playing = False
    count = 0
    update_freq = 10
    press_H = False
    press_S = False

    positions_Grass = set()
    positions_Sheep = set()

    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count  >= update_freq:
            count = 0
            positions_Grass = adjust_grid_Grass(positions_Grass)
            positions_Grass, positions_Sheep = adjust_grid_Sheep(positions_Grass, positions_Sheep)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if press_H:
                    x, y = pygame.mouse.get_pos()
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    pos = (col, row)

                    if pos in positions_Grass:
                        positions_Grass.remove(pos)

                    else:
                        positions_Grass.add(pos)
                
                if press_S:
                    x, y = pygame.mouse.get_pos()
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    pos = (col, row)
                    
                    if pos in positions_Sheep:
                        positions_Sheep.remove(pos)
                    
                    else:
                        positions_Sheep.add(pos)

            if  event.type == pygame.KEYDOWN:
                
                #Pause
                if event.key == pygame.K_SPACE:
                    playing = not playing

                #Clear mode
                if event.key == pygame.K_c:
                    positions_Grass = set()
                    positions_Sheep = set()
                    playing = False
                    count = 0

                #Générate mode
                if event.key == pygame.K_g:
                    positions_Grass = gen(random.randrange(10, 15) * GRID_WIDTH)
                    positions_Sheep = gen(random.randrange(7, 12) * GRID_WIDTH)

                    #Vérifie que les Sheep et la Grass ne sont pas sur la même case
                    for element in positions_Grass:
                        if element in positions_Sheep:
                            positions_Sheep.remove(element)

                #Grass mode
                if event.key == pygame.K_h:
                    press_H = not press_H
                    press_S = False
                    if press_H:
                        print("Grass mode activeted")    
                    else:
                        print("Grass mode desactiveted")  
                    
                #Sheep mode
                if event.key == pygame.K_s:
                    press_S = not press_S
                    press_H = False
                    if press_S:
                        print("Sheep mode activeted")    
                    else:
                        print("Sheep mode desactiveted")  
 
        screen.fill(Black)

        draw_grid()
        draw_grid_Grass(positions_Grass)
        draw_grid_Sheep(positions_Sheep)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

