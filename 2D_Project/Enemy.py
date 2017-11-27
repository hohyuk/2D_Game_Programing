import random

from pico2d import *

import Game_FrameWork




class Enemy:
    Enemy_SIZE = 64
    ENEMY_BULLETS = []
    image = None

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 600

        Enemy.image = load_image('image/enemy/Enemy.png')

    def get_pos(self):
        print(self.x,self.y)
        return self.x, self.y - 10

    def get_size(self):
        return self.x - 24, self.y - 24, self.x + 24, self.y + 24

    def draw_bb(self):
        draw_rectangle(*self.get_size ())

    def update(self, frame_time):
        self.y -= 0.5
        if self.y < 50 :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x,self.y)

