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

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruct_path(win, rows, cols, width, height,start, end, set_wall, set_path, came_from, current):
    set_path = set()
    show = True

    while current in came_from:
        current = came_from[current]
        set_path.add(current)
        if show:
            draw(win, rows, cols, width, height, start, end, set_wall, set_path)

        #Pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return set_path, False, True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return set_path, False, True

                if event.key == pygame.K_SPACE:
                    return set_path, True, False

                if event.key == pygame.K_s:
                    show = False
                
    return set_path,True , False

def algorithm(win, width, height, rows, cols, start, end, set_wall, run, stop, start_time):

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = []
    for x in range(cols):
        for y in range(rows):
            if (x, y) == start:
                g_score.append(0)
            else: 
                g_score.append(float("inf"))

    f_score = []
    for x in range(cols):
        for y in range(rows):

            if (x, y) == start:
                f_score.append(h(start, end))
            else: 
                f_score.append(float("inf"))

    open_set_hash = {start}
    delta = [-1, 0, 1]
    while not open_set.empty() and run and not stop:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            end_time = time.time()
            print(end_time - start_time)
            set_path, run , stop = reconstruct_path(win, rows, cols, width, height, start, end, set_wall, {}, came_from, current)
            return set_path, run, stop
        
        list_neighbors = []

        for delta_x in delta:
            for delta_y in delta:
                
                if (0 <= current[0] + delta_x <= cols -1) and (0 <= current[1] + delta_y <= rows -1) and not (current[0] + delta_x, current[1] + delta_y) in set_wall:
                    neighbors = (current[0] + delta_x, current[1] + delta_y)

                    if delta_x != 0 and delta_y != 0:
                        list_neighbors.append((neighbors, 1.5))   
                    else:
                        list_neighbors.append((neighbors, 1))
        
        for data_neigbors in list_neighbors:
            neigbors = data_neigbors[0]
            distance_neighbors = data_neigbors[1]

            temp_g__score = g_score[current[0] * rows + current[1]] + distance_neighbors

            if temp_g__score < g_score[neigbors[0] * rows + neigbors[1]]:
                came_from[neigbors] = current
                g_score[neigbors[0] * rows + neigbors[1]] = temp_g__score
                f_score[neigbors[0] * rows + neigbors[1]] = temp_g__score + h(neigbors, end)

                if neigbors not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neigbors[0] * rows + neigbors[1]], count, neigbors))
                    open_set_hash.add(neigbors)

        list_neighbors.clear()

        #Pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {}, False, True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return {}, False, True

                if event.key == pygame.K_SPACE:
                    return {}, True, False
                    
    return {}, run, stop

#Retrun the position in the grid, of the position of the mouse
def get_clicked_pos (pos, rows, cols, width, height):

    x, y = pos
    gap_x = width // cols
    gap_y = height // rows
    row = x // gap_x
    col = y // gap_y

    return row, col


#Add node in the grid
def add_node (width, height, rows, cols, start, end, set_wall):

    #Left click
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if (0 <= pos[0] <= width)  and (0 <= pos[1] <= height):
            row, col = get_clicked_pos(pos, rows, cols,  width, height)
            node = (row, col)

            if not start and node != end:
                start = node

            elif not end and node != start:
                end = node

            elif node != end and node != start:
                set_wall.add(node)
    
    return start, end, set_wall


#Delete node in the grid
def delete_node (width, height, rows, cols, start, end, set_wall):

    #Right click
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        if (0 <= pos[0] <= width)  and (0 <= pos[1] <= height):
            row, col = get_clicked_pos(pos, rows, cols, width, height)
            node = (row, col)

            if node == start:
                start = None

            if node == end:
                end = None

            if node in set_wall:
                set_wall.remove(node)

    return start, end, set_wall

#Main algorithm
def main (win, width, height):

    rows = 100
    cols = 100

    #Wall == -1
    set_wall = set()
    set_path = set()

    start = None
    end = None

    nb_door = 0

    run = True
    stop = False
    while run:

        #Pygame event
        for event in pygame.event.get():
            
            #Place the node in the grid
            start, end, set_wall = add_node(width, height, rows, cols,  start, end, set_wall)      #Left click
            start, end, set_wall = delete_node(width, height, rows, cols, start, end, set_wall)   #Right click

            #Quit pygame
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                
                #Make the  maze
                if event.key == pygame.K_g:
                    set_path.clear()
                    set_wall, start, end, run = make_maze(win, width, height, rows, cols, set_wall, nb_door)
                    
                #Search the smallest path
                if event.key == pygame.K_SPACE and start and end:
                    print("run")
                    start_time = time.time()
                    set_path, run, stop = algorithm(win, width, height, rows, cols, start, end, set_wall, run , stop, start_time)

                #New grid
                if event.key == pygame.K_n:   
                    set_path.clear()
                    set_wall.clear() 
                    start = None
                    end = None  
                    run = True
                    stop = False  
                    

                #Clear the grid
                if event.key == pygame.K_c:
                    set_path.clear()
                    run = True
                    stop = False 
                    
        draw(win, rows, cols, width, height, start, end, set_wall, set_path)

    pygame.quit()

main(WIN, WIDTH, HEIGHT)