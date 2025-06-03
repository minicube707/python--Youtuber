import pygame as pg
from object_3D import*
from camera import*
from projection import*

class SoftwarRender:
    def __init__(self) -> None:
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 2000, 1100
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES, pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.create_object()
    
    def create_object(self):
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])

        self.axes = Axes(self)
        self.axes.translate([0.7, 0.9, 0.7])

        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False
        self.world_axes.scale(2.5)
        self.world_axes.translate([0.001, 0.001, 0.001])

    def draw(self):
        self.screen.fill(pg.Color("darkslategray"))
        self.world_axes.draw()
        self.axes.draw()
        self.object.draw()
    
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
            self.camera.control()
            self.event()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    app = SoftwarRender()
    app.run()
