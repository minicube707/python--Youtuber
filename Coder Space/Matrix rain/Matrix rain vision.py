import pygame as pg
import numpy as np

class Matrix:

    def __init__(self, app, font_size = 8) -> None:
        self.app = app
        self.FONT_SIZE = font_size
        self.SIZE = self. ROWS, self.COLS = app.HEIGHT // font_size, app.WIDTH // font_size
        self.katakana = np.array([chr(int("0x030a0", 16) + i) for i in range(96)] + ["" for i in range(10)])
        self.font = pg.font.SysFont("ms mincho", font_size, bold=True)

        self.matrix = np.random.choice(self.katakana, self.SIZE)
        self.char_intervals = np.random.randint(25, 50, size=self.SIZE)
        self.cols_speed = np.random.randint(100, 500, size = self.SIZE)
        self.prerendered_chars = self.get_prerendered_chars()

        self.image = self.get_image("Desktop\\Document\\Programmation\\Python\\Youtuber\\Coder Space\\Matrix rain\\john-wick-chapter-two-2017.jpeg")

    def get_image(self, path_to_file):
        image = pg.image.load(path_to_file)
        image = pg.transform.scale(image, self.app.RES)
        pixel_array = pg.pixelarray.PixelArray(image)
        return pixel_array

    def get_prerendered_chars(self):
        char_colours = [(0, green, 0) for green in range(256)]
        prerendered_chars =  {}

        for char in self.katakana:
            prerendered_char = {(char, colour): self.font.render(char, True, colour) for colour in char_colours}
            prerendered_chars.update(prerendered_char)

        return prerendered_chars
        
    def run(self):
        frames = pg.time.get_ticks()
        self.change_chars(frames)
        self.shift_column(frames)
        self.draw()

    def shift_column(self, frames):
        num_cols = np.argwhere(frames  % self.cols_speed == 0)
        num_cols = num_cols[:, 1]
        num_cols = np.unique(num_cols)
        self.matrix[:, num_cols] = np.roll(self.matrix[:, num_cols], shift=1, axis=0)

    def change_chars(self, frames):
        mask = np.argwhere(frames % self.char_intervals == 0)
        new_chars = np.random.choice(self.katakana, mask.shape[0])
        self.matrix[mask[:, 0], mask[:, 1]] = new_chars

    def draw(self):
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char:
                    pos = x * self.FONT_SIZE, y * self.FONT_SIZE
                    _, red, green, blue = pg.Color(self.image[pos])

                    if red and green and blue:
                        colour = (red + green + blue) //3
                        colour = 220 if 160 < colour < 220 else colour
                        char = self.prerendered_chars[(char, (0, colour, 0))]
                        char.set_alpha(colour + 60)
                        self.app.surface.blit(char, pos)

class MatrixVision: 
    def __init__(self) -> None:
        self.RES = self.WIDTH, self.HEIGHT = 1900, 1100
        pg.init()
        self.screen = pg.display.set_mode(self.RES, pg.FULLSCREEN)
        self.surface = pg.Surface(self.RES)
        self.clock = pg.time.Clock()
        self.matrix = Matrix(self)

    def draw(self):
        self.surface.fill(pg.Color('black'))
        self.matrix.run()
        self.screen.blit(self.surface, (0, 0))
    
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()

    def run(self):
        while True:
            self.draw()
            self.event()
            pg.display.flip()
            pg.display.set_caption(str(self.clock.get_fps()))
            self.clock.tick()

if __name__ == "__main__":
    app = MatrixVision()
    app.run()