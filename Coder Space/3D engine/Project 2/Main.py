from object_3d import *
from camera import *
from projection import *
import pygame as pg
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)


class SoftwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 2000, 1100
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES, pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self) 
        self.object = self.get_object_from_file(os.path.join(module_dir, "t_34_obj.obj"))
        self.object.rotate_y(-math.pi / 4)

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
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


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()