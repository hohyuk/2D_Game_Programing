import random

from pico2d import *
from Bullet import EnummyBullet

import Game_FrameWork




class Enemy:
    Enemy_SIZE = 64
    ENEMY_BULLETS = []
    image = None

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 500

        Enemy.image = load_image('image/enemy/Enemy.png')

    def get_pos(self):
        print(self.x,self.y)
        return self.x, self.y

    def update(self, frame_time):
        self.y -= 1
        bullet = EnummyBullet(self.x,self.y)
        Enemy.ENEMY_BULLETS.append(bullet)

    def draw(self):
        self.image.draw(self.x,self.y)

