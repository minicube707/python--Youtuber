import pygame
import random
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path finding Algorithm")

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

class NODE:
    
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
        
    def is_closed(self):
        return self.colour == RED
        
    def is_open(self):
        return self.colour == GREEN
        
    def is_barrier(self):
        return self.colour == BLACK
                
    def is_start(self):
        return self.colour == ORANGE
        
    def is_end(self):
        return self.colour == CYAN
        
    def reset(self):
        self.colour =  WHITE

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour =  GREEN

    def make_barrier(self):
        self.colour = BLACK

    def make_start(self):
        self.colour = ORANGE

    def make_end(self):
        self.colour = CYAN

    def make_path(self):
        self.colour = PURPLE

    def make_build(self):
        self.colour = BLUE

    def draw_node(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []

        #Down
        if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        #Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        #Right
        if self.col < self.total_rows -1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        #Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

        
def mahe_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = NODE(i, j, gap, rows)
            grid[i].append(node)
    
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw_node(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def place_start(grid, rows):

    space = 0 
    while space%2 != 1:
        rand = random.randint(0, 1)
        space = random.randint(0, rows - 1)

    #Left
    if rand == 0:
        node = grid[0][space]
        node.make_start()
    
    #Right
    elif rand == 1:
        node = grid[rows - 1][space]
        node.make_start()

    #Up
    elif rand == 2:
        node = grid[space][0]
        node.make_start()

    #Down
    else:
        node = grid[space][rows -1]
        node.make_start()
    
    return node, rand

def place_end(grid, rows, current_node, rand):

    #Left
    placed_end = False
    i = 1
    if rand == 0:
        while (i <= rows -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:

                        if dx == 0 and dy == 0:
                            continue

                        state = grid[current_node.total_rows - 1 - i + dx][j + dy].is_barrier()
                        state_neighbors.append(state)

                if state_neighbors.count(True) == 7:
                    end_node = grid[current_node.total_rows - 1 - i][j]
                    end_node.make_end()
                    placed_end = True

                j +=1
            i +=1
                      
    #Right
    elif rand == 1:
        while (i <= rows -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue

                        state = grid[i + dx][j + dy].is_barrier()
                        state_neighbors.append(state)

                if state_neighbors.count(True) == 7:
                    end_node = grid[i][j]
                    end_node.make_end()
                    placed_end = True

                j +=1
            i +=1

    #Up
    elif rand == 2:
        while (i <= rows -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue

                        state = grid[j + dy][current_node.total_rows - 1 - i + dx].is_barrier()
                        state_neighbors.append(state)

                if state_neighbors.count(True) == 7:
                    end_node = grid[j][i]
                    end_node.make_end()
                    placed_end = True

                j +=1
            i +=1        

    #Down
    elif rand == 3:
        while (i <= rows -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue

                        state = grid[j + dx][i + dy].is_barrier()
                        state_neighbors.append(state)

                if state_neighbors.count(True) == 7:
                    end_node = grid[j][i]
                    end_node.make_end()
                    placed_end = True

                j +=1
            i +=1

    return grid, end_node

def function(grid, x1, y1, x2, y2, history_node, current_node):
    
    node = grid[x1][y1]
    node.reset()
    node = grid[x2][y2]
    node.reset()
    history_node.append(node)
    current_node.reset()
    current_node = node
    current_node.make_build()

    return history_node, current_node
    
def make_maze(grid, rows, win , width):

    for i in range(rows):
        for j in range(rows):
            node = grid[i][j]
            node.make_barrier()

    start_node, rand = place_start(grid, rows)
    
    current_node = start_node
    history_node =  []
    history_node.append(current_node)
    empty = True
    while empty:
      
        draw(win, grid, rows, width)
        list_direction =  [0, 1, 2, 3]

        for _ in range(5):

            if len(list_direction) > 0:
                orientation = random.choice(list_direction)
 
                #Down
                if orientation == 0:
                    if current_node.row +2 < current_node.total_rows -1 and grid[current_node.row + 2][current_node.col].is_barrier():
                        history_node, current_node = function(grid, current_node.row + 1, current_node.col, current_node.row + 2, current_node.col, history_node, current_node)

                    else:
                        list_direction.remove(orientation)

                #Up
                elif orientation == 1:
                    if current_node.row -2 > 0 and grid[current_node.row - 2][current_node.col].is_barrier():
                        history_node, current_node = function(grid, current_node.row - 1, current_node.col, current_node.row - 2, current_node.col, history_node, current_node)

                    else:
                        list_direction.remove(orientation)

                #Right
                elif orientation == 2:
                    if current_node.col + 2 < current_node.total_rows -1 and grid[current_node.row][current_node.col +2].is_barrier():
                        history_node, current_node = function(grid, current_node.row, current_node.col + 1, current_node.row, current_node.col + 2, history_node, current_node)


                    else:
                        list_direction.remove(orientation)

                #Left
                elif orientation == 3:
                    if current_node.col - 2 > 0 and grid[current_node.row][current_node.col -2].is_barrier():
                        history_node, current_node = function(grid, current_node.row, current_node.col - 1, current_node.row, current_node.col - 2, history_node, current_node)

                    else:
                        list_direction.remove(orientation)

            else:
                history_node.pop(-1)
                if len(history_node) > 0:
                    current_node.reset()
                    current_node = history_node[-1]
                    current_node.make_build()

                    if current_node == start_node:
                        empty = False

                else:
                    empty = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return grid, start_node, None, True, False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return grid, start_node, None, True, False

    start_node.make_start()
    grid, end_node = place_end(grid, rows, current_node, rand)

    return grid, start_node, end_node, True, True

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, current, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neigbors in current.neighbors:
            temp_g__score = g_score[current] + 1

            if temp_g__score < g_score[neigbors]:
                came_from[neigbors] = current
                g_score[neigbors] = temp_g__score
                f_score[neigbors] = temp_g__score + h(neigbors.get_pos(), end.get_pos())

                if neigbors not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neigbors], count, neigbors))
                    open_set_hash.add(neigbors)
                    neigbors.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def main(win, width):
    rows = 50
    grid = mahe_grid(rows, width)
    run = True
    finish = False

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            while not finish:
                grid, start, end, finish,  run = make_maze(grid, rows, win , width)

            if run:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        grid = mahe_grid(rows, width)

                    if event.key == pygame.K_SPACE:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)

                        algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

    pygame.quit()


main(WIN, WIDTH)