
import os
import pygame as pg
from random import choice, randrange


class Symbol:
    def __init__(self, x, y, speed, font) -> None:
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(font)           #A katakana
        self.interval = randrange(10, 27)
        self.invisible = False

    def draw(self, font):
        frame = pg.time.get_ticks()
        if not frame % self.interval:
            self.value = choice(font)       #A katakana

        if self.y < HEIGHT:
            self.y = self.y + self.speed
        else:
            self.y = -FONT_SIZE
            self.invisible = True

        surface.blit(self.value, (self.x, self.y))

class SymbolColumn:

    def __init__(self, x, y, para_speed, para_column) -> None:       
        self.column_heifht = randrange(para_column[0], para_column[1])
        self.speed = randrange(para_speed[0], para_speed[1])
        self.x = x
        self.y = y
        self.font = FONT(FONT_SIZE, FONT_GAP)       #Create a font with a random font_size
        self.font_size = self.font.get_size()
        self.symbols = [Symbol(x, i, self.speed, self.font.get_katakana()[0]) for i in range(y, y -FONT_SIZE * self.column_heifht, -FONT_SIZE)]
    
    def draw(self):
        column_invisible = True

        for symbol in self.symbols:
            if not symbol.invisible:
                column_invisible = False
        
        #Reset
        if column_invisible:
            self.column_heifht = randrange(para_column[0], para_column[1])
            self.speed = randrange(para_speed[0], para_speed[1])
            self.font = FONT(FONT_SIZE, FONT_GAP)

            self.font_size = self.font.get_size()
            self.symbols = [Symbol(self.x, i, self.speed, self.font.get_katakana()[0]) for i in range(self.y, self.y -FONT_SIZE * self.column_heifht, -FONT_SIZE)]

            for symbol in self.symbols:
                symbol.invisible = False

        #For each character if it's this colour is light green alse green
        for i, symbol in enumerate(self.symbols):
            if i and not symbol.invisible:
                symbol.draw(self.font.get_katakana()[0])
            elif not symbol.invisible:
                symbol.draw(self.font.get_katakana()[1])


class FONT:

    def __init__(self, size, gap) -> None:

        self.font_size = size + randrange(-gap, gap)
        font = pg.font.SysFont("ms mincho", self.font_size, bold=True)
        green_katakana = [font.render(char, True, (0, randrange(128, 256), 0)) for char in katakana]
        light_green_katakana = [font.render(char, True, pg.Color("lightgreen")) for char in katakana]

        #Create a list with a green character sublist and a light green character sublist
        list_katakana = []
        list_katakana.append([green_katakana, light_green_katakana])
        list_katakana = list_katakana[0]
        self.list_katakana = list_katakana

    def get_katakana(self):
        return self.list_katakana
    
    def get_size(self):
        return self.font_size


os.environ["VIDEO_CENTERED"] = "1"
RES = WIDTH, HEIGHT = 2000, 1200
FONT_SIZE = 30
FONT_GAP = 20
set_alpha_value = 100
alpha_value = set_alpha_value

para_speed = 3, 7
para_column = 8, 16

blurry_effect = True

pg.init()
screen = pg.display.set_mode((RES))
surface = pg.Surface(RES)
surface.set_alpha(alpha_value)
clock = pg.time.Clock()
pg.mouse.set_visible(False)

katakana = [chr(int("0x30a0", 16) + i) for i in range (96)]

symbol_columns = [SymbolColumn(x, 0, para_speed, para_column) for x in range (0, WIDTH, FONT_SIZE)]

while True:
    screen.blit(surface,( 0, 0))
    surface.fill(pg.Color("black"))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()

            if event.key == pg.K_SPACE:
                blurry_effect = True
                alpha_value = 0
            
    if not pg.time.get_ticks() % 20 and alpha_value < set_alpha_value and blurry_effect:
        alpha_value += 6
        surface.set_alpha(alpha_value)

    if set_alpha_value < alpha_value:
        alpha_value = set_alpha_value
        blurry_effect = False

    symbol_columns.sort(key= lambda symobol: symobol.font_size)
    [symbol_column.draw() for symbol_column in symbol_columns]

    pg.display.flip()
    clock.tick(60)