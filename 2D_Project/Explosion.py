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
        PlayerExplosion.image = load_image('image/explosion/explosion1.png')

    def update(self,frame_time):
        self.time += frame_time * 10
        if self.frame < 6 :
            if self.time > 1:
                self.frame = (self.frame + 1) % 7
                self.time = 0

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


class BigExplosion(Explosion):
    SIZE = 160

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.state =0
        self.time = 0
        BigExplosion.image = load_image('image/explosion/explosion3.png')

    def update(self, frame_time):
        self.time += frame_time*30

        if self.time > 1 :
            if self.frame >= 3:
                self.state += 1
            self.frame = (self.frame + 1) % 4
            self.time = 0

        if self.state == 4:
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * BigExplosion.SIZE, self.state * BigExplosion.SIZE
                             , BigExplosion.SIZE, BigExplosion.SIZE, self.x, self.y)


class BossExplosion(Explosion):
    SIZE = 320

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.state = 0
        self.time = 0
        BossExplosion.image = load_image('image/explosion/explosion4.png')

    def update(self,frame_time):
        self.time += frame_time

        if self.time > 0.3:
            if self.frame >= 3:
                self.state += 1
            self.frame = (self.frame + 1) % 4
            self.time = 0

        if self.state == 4:
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * BossExplosion.SIZE, self.state * BossExplosion.SIZE
                             , BossExplosion.SIZE, BossExplosion.SIZE, self.x, self.y)