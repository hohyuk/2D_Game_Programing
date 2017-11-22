import random

from pico2d import *

import Game_FrameWork


class Enemy:
    Enemy_SIZE = 64

    image = None

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 500

        Enemy.image = load_image('image/enemy/Enemy.png')


    def update(self, frame_time):
        self.y -= 1

    def draw(self):
        self.image.draw(self.x,self.y)

