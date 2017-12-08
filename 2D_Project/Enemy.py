import random

from pico2d import *
from Missile import EnummyMissile
import Game_FrameWork


class Enemy:
    Enemy_SIZE = 64
    ENEMY_BULLETS = []
    image = None
    missileSound = None

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 600

        Enemy.image = load_image('image/enemy/Enemy.png')

        if Enemy.missileSound == None:
            Enemy.missileSound = load_wav('sound/EnemyMissile.wav')
            Enemy.missileSound.set_volume(64)

    def get_pos(self):
        self.missileSound.play()
        return self.x, self.y - 10

    def get_size(self):
        return self.x - 24, self.y - 24, self.x + 24, self.y + 24

    def draw_box(self):
        draw_rectangle(*self.get_size ())

    def update(self, frame_time):
        self.y -= 0.5
        if self.y < 0 :
            return True
        else :
            return False



    def draw(self):
        self.image.draw(self.x,self.y)

