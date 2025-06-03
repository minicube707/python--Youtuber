import pygame
import  random

pygame.init()

Black = (0, 0, 0)
Grey = (128, 128, 128)
Yellow = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH =  WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

def gen(number):
    #random.randrange(0, 1)
    # Utilisez la fonction random.randrange(a, b) pour obtenir un nombre entier aléatoire entre a (inclus) et b (exclus).
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(number)])

def draw_grid(positions):

    for position in positions:
        column, row = position
        top_left = (column * TILE_SIZE, row *  TILE_SIZE)
        pygame.draw.rect(screen, Yellow, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, Black, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for column  in range(GRID_WIDTH):
        pygame.draw.line(screen, Black, (column * TILE_SIZE, 0), (column * TILE_SIZE, HEIGHT))

def adjust_grid(positions):

    # set()
    #Un ensemble est une collection non ordonnée d’éléments.
    #Chaque élément dans un ensemble est unique (pas de doublons).
    #Les éléments d’un ensemble doivent être immuables (c’est-à-dire qu’ils ne peuvent pas être modifiés).
    #Cependant, l’ensemble lui-même est modifiable ; vous pouvez ajouter ou supprimer des éléments.
    #Les ensembles peuvent être utilisés pour effectuer des opérations mathématiques telles que l’union, l’intersection et la différence symétrique.

    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2,3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions

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
    update_freq = 5

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count  >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                
                else:
                    positions.add(pos)

            if  event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4,8) * GRID_WIDTH)

        screen.fill(Grey)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

