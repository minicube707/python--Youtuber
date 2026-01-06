import pygame as pg
from random import randint
from copy import deepcopy
import numpy as np
from numba import njit

RES = WIDTH, HEIGTH = 1900, 1100
TILE = 2
W, H = WIDTH // TILE, HEIGTH // TILE
FPS = 10

pg.init()
surface = pg.display.set_mode(RES, pg.FULLSCREEN)
clock = pg.time.Clock()

next_field = np.array([[0 for i in range(W)] for j in range(H)])
current_field = np.array([[randint(0, 1) for i in range(W)] for j in range(H)])

@njit(fastmath = True)
def check_cell(current_field, next_field):
   
    res = []
    for x in range(W):
        for y in range(H):
           
            count = 0
            for  j in range(y-1, y+2):
                for  i in range(x-1, x+2):
                    if current_field[j % H][i % W] == 1:
                        count +=1
            
            if current_field[y][x] == 1:
                count -=1
            
                if count == 2 or count == 3:
                    next_field[y][x] = 1
                    res.append((x, y))

                else:
                    next_field[y][x] = 0
            
            else:
                if count == 3:
                    next_field[y][x] = 1
                    res.append((x, y))
                
                else:
                    next_field[y][x] = 0
    
    return next_field, res
        
def event():

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()


while True:

    surface.fill(pg.Color("black"))
    event()

    #Draw life
    next_field, res = check_cell(current_field, next_field)
    [pg.draw.rect(surface, pg.Color("white"), (x*TILE +1, y*TILE+1, TILE-1, TILE-1)) for x,y in res]

    current_field = deepcopy(next_field)

    pg.display.flip()
    clock.tick(FPS)
    

    