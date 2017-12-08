from pico2d import *

import Game_FrameWork


class Explosion:
    image = None


class PlayerExplosion(Explosion):
    SIZE = 128
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.time = 0
        EnemyExplosion.image = load_image('image/explosion/explosion1.png')

    def update(self,frame_time):
        self.frame = (self.frame + 1) % 6

        if self.frame == 5:
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * PlayerExplosion.SIZE, 0
                             , PlayerExplosion.SIZE, PlayerExplosion.SIZE, self.x, self.y)


class EnemyExplosion(Explosion):
    SIZE = 71

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.time = 0
        EnemyExplosion.image = load_image('image/explosion/explosion2.png')

    def update(self, frame_time):
        self.time += frame_time*30
        if self.time > 1 :
            self.frame = (self.frame + 1) % 12
            self.time = 0

        if self.frame == 11:
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * EnemyExplosion.SIZE, 0
                             , EnemyExplosion.SIZE, EnemyExplosion.SIZE, self.x, self.y)