import pygame
import random
from queue import PriorityQueue
import time
import math

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flood fill Path finding Algorithm")


#Color in RGB
BLACK =         (0, 0, 0)
GREY =          (128, 128, 128)
WHITE =         (255, 255, 255)

RED =           (255, 0, 0)
GREEN =         (0, 255, 0)
BLUE =          (0, 0, 255)

YELLOW =        (255, 255, 0)
CYAN =          ( 0, 255, 255)
PURPLE =        (255, 0, 255)

ORANGE =        (255, 165, 0)
PINK =          (255,25,179)


#Draw left grid,this represent the world
def drawn_global_vision(win, width, height, rows, cols, start, end, set_wall, set_path):
    gap_x = width // cols
    gap_y = height // rows
    

    for wall in set_wall:
        pygame.draw.rect(win, BLACK, (wall[0]*gap_x, wall[1]*gap_y, gap_x, gap_y))
    
    for paht in set_path:
        pygame.draw.rect(win, PURPLE, (paht[0]*gap_x, paht[1]*gap_y, gap_x, gap_y))

    if isinstance(start, tuple):  
        pygame.draw.rect(win, ORANGE, (start[0]*gap_x, start[1]*gap_y, gap_x, gap_y))

    if isinstance(end, tuple):
        pygame.draw.rect(win, CYAN, (end[0]*gap_x, end[1]*gap_y,  gap_x, gap_y))


#Draw the grid
def draw_grid (win, rows, cols, width, height):
    gap_x = width // cols
    gap_y = height // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap_y), (width, i * gap_y))

        for j in range(cols):
            pygame.draw.line(win, GREY, (j * gap_x, 0), (j * gap_x, height))



#Draw the window
def draw (win, rows, cols, width, height, start, end, set_wall, set_path):

    #Initialisation
    WIN.fill(WHITE)
    drawn_global_vision(win, width, height, rows, cols, start, end, set_wall, set_path)
    draw_grid(win, rows, cols, width, height)

    pygame.draw.line(win, BLACK, (width, 0), (width, height), 3)
    pygame.display.update()


#Make the maze
def make_maze(win, width, height, rows, cols, set_wall, nb_door):

    #Fill wall the maze with wall
    for i in range(rows):
        for j in range(cols):
            set_wall.add((j, i))

    #Initialsation 
    start_node, rand = place_start(rows, cols)
    set_wall.remove(start_node)


    current_node = start_node
    history_node =  []
    history_node.append(current_node)
    show = True

    #While there is node in history_node, the maze isn't fill
    empty = True
    while empty:
        list_direction =  [0, 1, 2, 3]

        if show:
            draw(win, rows, cols, width, height, start_node, {}, set_wall, {})
        
        for _ in range(5):
            
            #Search  if the neighbors are walls, in the four direction
            if len(list_direction) > 0:
                orientation = random.choice(list_direction)
 
                #Right
                if orientation == 0:
                    #Is the neighbors is a wall ?
                    if current_node[0] +2 < cols -1 and (current_node[0] + 2, current_node[1]) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0] + 1, current_node[1], current_node[0] + 2, current_node[1], history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

                #Left
                elif orientation == 1:
                    #Is the neighbors is a wall ?
                    if current_node[0] -2 > 0 and (current_node[0] - 2 ,current_node[1]) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0] - 1, current_node[1], current_node[0] - 2, current_node[1], history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

                #UP
                elif orientation == 2:
                    #Is the neighbors is a wall ?
                    if current_node[1] + 2 < rows -1 and (current_node[0], current_node[1] +2) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0], current_node[1] + 1, current_node[0], current_node[1] + 2, history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

                #Down
                elif orientation == 3:
                    #Is the neighbors is a wall ?
                    if current_node[1] - 2 > 0 and (current_node[0], current_node[1] -2) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0], current_node[1] - 1, current_node[0], current_node[1] - 2, history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

            #All the directions are taken
            #Go back in the path
            else:
                history_node.pop(-1)
                if len(history_node) > 0:
                    current_node = history_node[-1]

                    if current_node == start_node:
                        empty = False

                else:
                    empty = False

        #Pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return set_wall, start_node, None, False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return set_wall, start_node, None, False

                if event.key == pygame.K_s:
                    show = False
                
    end_node = place_end(set_wall, rows, cols, rand)

   #Add the door
    for _ in  range(nb_door):
        reset = True
        while reset:
            x = random.randint(1, rows - 2)
            y = random.randint(1, rows - 2)
            if (x, y) in set_wall and (x, y) != start_node and (x, y) != end_node:

                if ((x-1, y) in set_wall and (x+1, y) in set_wall) or ((x, y-1) in set_wall and  (x, y+1) in set_wall):
                    set_wall.remove((x, y))
                    reset = False

                    if show:
                        draw(win, rows, cols, width, height, start_node, {}, set_wall, {})
                        
            
            #Pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return set_wall, start_node, None, False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return set_wall, start_node, None, False

    return set_wall, start_node, end_node, True


#Create the path when you built the maze
def function(set_wall, x1, y1, x2, y2, history_node):
    
    node = (x1, y1)
    set_wall.remove(node)
    node = (x2, y2) 
    set_wall.remove(node)
    history_node.append(node)

    return history_node, node, set_wall


#Place the start node
def place_start(rows, cols):

    rand = random.randint(0, 3)
    if rand == 0 or rand == 1:
        
        space = 0 
        while space%2 != 1:
            space = random.randint(0, cols - 1)

        #Left
        if rand == 0:
            node = (space, 0)
    
        #Right
        else:
            node = (space, cols - 1)

    else:
        space = 0 
        while space%2 != 1:
            space = random.randint(0, rows - 1)

        #Up
        if rand == 2:
            node = (0, space)

        #Down
        else:
            node = (rows - 1, space)
    
    return node, rand


#Place the end node
def place_end(set_wall, rows, cols, rand):

    #Left
    placed_end = False
    i = 1
    if rand == 0:
        while (i <= cols -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = 0
                #For the eight neigbords of the node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        
                        #If is itself pass
                        if dx == 0 and dy == 0:
                            continue
                        
                        #If the neighbors is a barreir 
                        if (cols - 1 - i + dx, j + dy) in set_wall:
                            state_neighbors += 1

                #If the node has 7 node who is barrier next to him, place the end node
                if state_neighbors == 7:
                    end_node = (cols - 1 - i, j)
                    placed_end = True

                j +=1
            i +=1
                      
    #Right
    elif rand == 1:
        while (i <= cols -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = 0
                #For the eight neigbords of the node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        
                        #If the neighbors is a barreir 
                        if (i + dx, j + dy) in set_wall:
                            state_neighbors += 1

                if state_neighbors == 7:
                    end_node = (i, j)
                    placed_end = True

                j +=1
            i +=1

    #Up
    elif rand == 2:
        while (i <= cols -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = 0
                #For the eight neigbords of the node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        
                        #If the neighbors is a barreir 
                        if (j + dy, cols - 1 - i + dx) in set_wall:
                            state_neighbors += 1

                #If the node has 7 node who is barrier next to him, place the end node
                if state_neighbors == 7:
                    end_node = (j, cols - 1 - i)
                    placed_end = True

                j +=1
            i +=1        

    #Down
    elif rand == 3:
        while (i <= cols -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = 0
                #For the eight neigbords of the node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        
                        #If the neighbors is a barreir 
                        if (j + dx, i + dy) in set_wall:
                            state_neighbors += 1

                #If the node has 7 node who is barrier next to him, place the end node
                if state_neighbors == 7:
                    end_node = (j, i)
                    placed_end = True

                j +=1
            i +=1

    return  end_node

#Main algorithm
def main (win, width, height):

    #Wall == -1
    set_wall = set()
    set_path = set()

    rows = 100
    cols = 100
    nb_door = 10

    set_wall, start, end, run = make_maze(win, width, height, rows, cols, set_wall, nb_door)
    
    run = True

    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            
            #Clear the grid
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    set_path.clear()
                    run = True
                    set_wall, start, end, run = make_maze(win, width, height, rows, cols, set_wall, nb_door)

        draw(win, rows, cols, width, height, start, end, set_wall, set_path)

    pygame.quit()

main(WIN, WIDTH, HEIGHT)