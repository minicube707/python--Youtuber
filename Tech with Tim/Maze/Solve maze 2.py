import pygame
import random
import time

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
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
def drawn_global_vision(win, width, rows, start, end, set_wall, pathfinder, set_path):
    gap = width // rows
    
    for path in set_path:
        pygame.draw.rect(win, GREEN, (path[1]*gap, path[0]*gap,  gap, gap))

    for wall in set_wall:
        pygame.draw.rect(win, BLACK, (wall[1]*gap, wall[0]*gap,  gap, gap))
    
    if isinstance(pathfinder, tuple):
        pygame.draw.rect(win, BLUE, (pathfinder[1]*gap, pathfinder[0]*gap,  gap, gap))

    if isinstance(start, tuple):  
        pygame.draw.rect(win, ORANGE, (start[1]*gap, start[0]*gap,  gap, gap))

    if isinstance(end, tuple):
        pygame.draw.rect(win, CYAN, (end[1]*gap, end[0]*gap,  gap, gap))


#Draw the grid
def draw_grid (win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))



#Draw the window
def draw (win, rows, width, start, end, set_wall, pathfinder, set_path):

    #Initialisation
    WIN.fill(WHITE)
    drawn_global_vision(win, width, rows, start, end, set_wall, pathfinder, set_path)
    draw_grid(win, rows, width)

    pygame.draw.line(win, BLACK, (width, 0), (width, width), 3)
    pygame.display.update()


#Make the maze
def make_maze(win, width, rows, set_wall, nb_door):

    #Fill wall the maze with wall
    for i in range(rows):
        for j in range(rows):
            set_wall.add((i, j))

    #Initialsation     
    start_node, rand = place_start(rows)
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
            draw(win, rows, width, start_node, {}, set_wall, {}, {})
        
        for _ in range(5):
            
            #Search  if the neighbors are walls, in the four direction
            if len(list_direction) > 0:
                orientation = random.choice(list_direction)
 
                #Down
                if orientation == 0:
                    #Is the neighbors is a wall ?
                    if current_node[0] +2 < rows -1 and (current_node[0] + 2, current_node[1]) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0] + 1, current_node[1], current_node[0] + 2, current_node[1], history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

                #Up
                elif orientation == 1:
                    #Is the neighbors is a wall ?
                    if current_node[0] -2 > 0 and (current_node[0] - 2 ,current_node[1]) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0] - 1, current_node[1], current_node[0] - 2, current_node[1], history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

                #Right
                elif orientation == 2:
                    #Is the neighbors is a wall ?
                    if current_node[1] + 2 < rows -1 and (current_node[0], current_node[1] +2) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0], current_node[1] + 1, current_node[0], current_node[1] + 2, history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

                #Left
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
                
    end_node = place_end(set_wall, rows, rand)

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
                        draw(win, rows, width, start_node, {}, set_wall, {}, {})
                        
            
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
def place_start(rows):

    space = 0 
    while space%2 != 1:
        rand = random.randint(0, 3)
        space = random.randint(0, rows - 1)

    #Left
    if rand == 0:
        node = (0, space )
    
    #Right
    elif rand == 1:
        node = (rows - 1, space)

    #Up
    elif rand == 2:
        node = (space, 0)

    #Down
    else:
        node = (space, rows - 1)
    
    return node, rand


#Place the end node
def place_end(set_wall, rows, rand):

    #Left
    placed_end = False
    i = 1
    if rand == 0:
        while (i <= rows -1) and not placed_end:
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
                        if (rows - 1 - i + dx, j + dy) in set_wall:
                            state_neighbors += 1

                #If the node has 7 node who is barrier next to him, place the end node
                if state_neighbors == 7:
                    end_node = (rows - 1 - i, j)
                    placed_end = True

                j +=1
            i +=1
                      
    #Right
    elif rand == 1:
        while (i <= rows -1) and not placed_end:
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
        while (i <= rows -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = 0
                #For the eight neigbords of the node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        
                        #If the neighbors is a barreir 
                        if (j + dy, rows - 1 - i + dx) in set_wall:
                            state_neighbors += 1

                #If the node has 7 node who is barrier next to him, place the end node
                if state_neighbors == 7:
                    end_node = (j, rows - 1 - i)
                    placed_end = True

                j +=1
            i +=1        

    #Down
    elif rand == 3:
        while (i <= rows -1) and not placed_end:
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


#Retrun the position in the grid, of the position of the mouse
def get_clicked_pos (pos, rows, width):

    x, y = pos
    gap = width // rows
    row = x // gap
    col = y // gap

    return row, col


#Add node in the grid
def add_node (width, rows, start, end, set_wall):

    #Left click
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if (0 <= pos[0] <= width)  and (0 <= pos[1] <= width-1):
            row, col = get_clicked_pos(pos, rows, width)
            node = (col, row)

            if not start and node != end:
                start = node

            elif not end and node != start:
                end = node

            elif node != end and node != start:
                set_wall.add(node)
    
    return start, end, set_wall


#Delete node in the grid
def delete_node (width, rows, start, end, set_wall):

    #Right click
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        if (0 <= pos[0] <= width)  and (0 <= pos[1] <= width):
            row, col = get_clicked_pos(pos, rows, width)
            node = (col, row)

            if node == start:
                start = None

            if node == end:
                end = None

            if node in set_wall:
                set_wall.remove(node)

    return start, end, set_wall


def solve_maze(win, width, rows, start, end, set_wall):
    current_node = start
    set_path = set()
    run = True

    #Pygame event
    while current_node != end and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                #Left
                if event.key == pygame.K_LEFT and current_node[1] > 0 and not (current_node[0], current_node[1] - 1) in set_wall:
                    current_node = (current_node[0], current_node[1] - 1)

                #Right
                elif event.key == pygame.K_RIGHT and current_node[1] < rows -1 and not (current_node[0], current_node[1] + 1) in set_wall:
                    current_node = (current_node[0], current_node[1] + 1)

                #Up
                elif event.key == pygame.K_UP and current_node[0] > 0 and not (current_node[0] - 1, current_node[1]) in set_wall:
                    current_node = (current_node[0] - 1, current_node[1])

                #Down
                elif event.key == pygame.K_DOWN and current_node[0] < rows -1 and not (current_node[0] + 1, current_node[1]) in set_wall:
                    current_node =(current_node[0] + 1, current_node[1])

        if not current_node in set_path:
            set_path.add(current_node)

        draw(win, rows, width, start, end, set_wall, current_node, set_path)

    return run, set_path
        
#Main algorithm
def main (win , width):

    rows = 20

    #Wall == -1
    set_wall = set()
    set_path = set()
    start = None
    end = None
    
    nb_door = 0

    game = False
    run = True
    while run:

        #Pygame event
        for event in pygame.event.get():
            
            #Place the node in the grid
            start, end, set_wall = add_node(width, rows, start, end, set_wall)      #Left click
            start, end, set_wall = delete_node(width, rows, start, end, set_wall)   #Right click

            #Quit pygame
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                
                #Make the  maze
                if event.key == pygame.K_g:
                    set_path.clear()
                    set_wall, start, end, run = make_maze(win, width, rows, set_wall, nb_door)
                    
                #Search the smallest path
                if (event.key == pygame.K_SPACE and start and end) or game:
                    set_path.clear()
                    print("Go")
                    start_time = time.time()
                    run, set_path = solve_maze(win, width, rows, start, end, set_wall)
                    end_time = time.time()
                    print("Vous avez mis ", end_time - start_time)
                        
                #New grid
                if event.key == pygame.K_n:   
                    set_wall.clear() 
                    set_path.clear()
                    start = None
                    end = None  
                    run = True
                    

                #Clear the grid
                if event.key == pygame.K_c:
                    set_path.clear()
                    run = True
    
        draw(win, rows, width, start, end, set_wall, {}, set_path)

    pygame.quit()

main(WIN, WIDTH)