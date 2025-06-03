import pygame as pg
from collections import deque

class Ant:
    def __init__(self, app, pos, colour) -> None:
        self.app = app
        self.colour = colour
        self.x, self.y = pos
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])


    def run(self):
        value = self.app.grid[self.y][self.x]
        self.app.grid[self.y][self.x] = not value   

        SIZE = self.app.CELL_SIZE
        rect = self.x * SIZE, self.y * SIZE, SIZE -1, SIZE-1
        if value:
            pg.draw.rect(self.app.screen, pg.Color("white"), rect)
        else:
            pg.draw.rect(self.app.screen, self.colour, rect)
        
        self.increments.rotate(1) if value else self.increments.rotate(-1)
        dx, dy = self.increments[0]
        self.x = (self.x + dx) % self.app.COLS
        self.y = (self.y + dy) % self.app.ROWS


class App:
    def __init__(self, WIDTH=1900, HEIGHT=1000, CELL_SIZE=12) -> None:
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT], pg.FULLSCREEN)
        self.clock = pg.time.Clock()

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT// CELL_SIZE, WIDTH // CELL_SIZE
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]

        self.ant = Ant(app=self, pos=[self.COLS//2, self.ROWS//2], colour=pg.Color("orange"))
        
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
    
    def run(self):
        while True:
            self.ant.run()
            self.event()
            pg.display.flip()
            self.clock.tick()

if __name__ == "__main__":
    app = App()
    app.run()