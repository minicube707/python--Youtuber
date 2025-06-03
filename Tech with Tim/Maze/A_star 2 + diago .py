import pygame
from queue import PriorityQueue
import math

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
TURQUOISE =     (64, 224, 208)
VIOLET =        (128, 0, 128)

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
        return self.colour == TURQUOISE
    
    def is_path(self):
        return self.colour == VIOLET
        
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
        self.colour = TURQUOISE

    def make_path(self):
        self.colour = VIOLET

    def draw_node(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        delta = [-1, 0, 1]

        for delta_x in delta:
            for delta_y in delta:
                
                if (0 <= self.row + delta_y <= self.total_rows -1) and (0 <= self.col + delta_x <= self.total_rows -1) and not grid[self.row + delta_y][self.col + delta_x].is_barrier():
                    neighbors = grid[self.row + delta_y][self.col + delta_x]

                    if delta_x != 0 and delta_y != 0:
                        self.neighbors.append((neighbors, 1.41))   
                    else:
                        self.neighbors.append((neighbors, 1))   
                    
        
        
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

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
        
        for data_neigbors in current.neighbors:
            neigbors = data_neigbors[0]
            distance_neighbors = data_neigbors[1]

            temp_g__score = g_score[current] + distance_neighbors

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


def make_grid(rows, width):
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

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = x // gap
    col = y // gap

    return row, col

def main(win, width):
    rows = 50
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, rows, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            
            #Left
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if (0 <= pos[0] <= width)  and (0 <= pos[1] <= width):
                    row, col = get_clicked_pos(pos, rows, width)
                    node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()
                
                elif node != end and node != start:
                    node.make_barrier()

            #Right
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if (0 <= pos[0] <= width)  and (0 <= pos[1] <= width):
                    row, col = get_clicked_pos(pos, rows, width)
                    node = grid[row][col]
                    node.reset()

                if node == start:
                    start = None
                
                if node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and  start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_n:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
                
                if event.key == pygame.K_c:
                    for row in grid:
                        for node in row:
                            if node.is_open() or node.is_closed() or node.is_path() :
                                node.reset()

    pygame.quit()


main(WIN, WIDTH)