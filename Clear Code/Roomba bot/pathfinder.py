
from queue import PriorityQueue
import math
import pygame
import sys

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruct_path(came_from, current, start):
    set_path = []

    while current in came_from:
        set_path.append(current)
        current = came_from[current]

        #Pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    set_path.append(start)
    
    return set_path[::-1]

def algorithm(rows, cols, start, end, set_wall):

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
    while not open_set.empty():
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            return reconstruct_path(came_from, current, start)
        
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
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
    return {}