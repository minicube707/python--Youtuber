
import os
import pygame as pg
from random import choice, randrange


class Symbol:
    def __init__(self, x, y, speed) -> None:
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_katakana)
        self.interval = randrange(5, 27)

    def draw(self, color):
        frame = pg.time.get_ticks()
        if not frame % self.interval:
            self.value = choice(green_katakana  if color == "green" else light_green_katakana)
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE
        surface.blit(self.value, (self.x, self.y))

class SymbolColumn:

    def __init__(self, x, y) -> None:       
        self.column_heifht = randrange(8, 16)
        self.speed = randrange(2, 6)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y -FONT_SIZE * self.column_heifht, -FONT_SIZE)]
    
    def draw(self):
        [symbol.draw("green") if i else symbol.draw("lightgreen") for i, symbol in enumerate(self.symbols)]




os.environ["VIDEO_CENTERED"] = "1"
RES = WIDTH, HEIGHT = 2000, 1200
FONT_SIZE = 40
alpha_value = 120
 
pg.init()
screen = pg.display.set_mode((RES), pg.FULLSCREEN)
surface = pg.Surface(RES)
surface.set_alpha(alpha_value)
clock = pg.time.Clock()
pg.mouse.set_visible(False)

katakana = [chr(int("0x30a0", 16) + i) for i in range (96)]
font = pg.font.SysFont("ms mincho", FONT_SIZE, bold=True)
green_katakana = [font.render(char, True, (0, randrange(160, 256), 0)) for char in katakana]
light_green_katakana = [font.render(char, True, pg.Color("lightgreen")) for char in katakana]

symbol_columns = [SymbolColumn(x, 0) for x in range (0, WIDTH, FONT_SIZE)]

while True:
    screen.blit(surface,( 0, 0))
    surface.fill(pg.Color("black"))

    [symbol_column.draw() for symbol_column in symbol_columns]

    [exit() for event in pg.event.get() if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)]

    pg.display.flip()
    clock.tick(60)