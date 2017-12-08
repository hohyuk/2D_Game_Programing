import random

from pico2d import *

import Game_FrameWork


class Enemy:
    Enemy_SIZE = 64

    PIXEL_PER_METER = (10.0 / 22.25)  # 10 pixel 22.25m -> 22.25cm -> 73fit
    Enemy_SPEED_KMPH = 1500.0  # 2마하 -> 약 2000km
    Enemy_SPEED_MPM = (Enemy_SPEED_KMPH * 1000.0 / 60.0)
    Enemy_SPEED_MPS = (Enemy_SPEED_MPM / 60.0)
    Enemy_SPEED_PPS = (Enemy_SPEED_MPS * PIXEL_PER_METER)
    image = None
    missileSound = None

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 600
        self.time = 0
        Enemy.image = load_image('image/enemy/Enemy.png')

        if Enemy.missileSound == None:
            Enemy.missileSound = load_wav('sound/EnemyMissile.wav')
            Enemy.missileSound.set_volume(64)

    def get_pos(self):
        self.missileSound.play()
        return self.x, self.y - 10

    def getMissileTime(self):
        return self.time

    def setMissileTime(self,reset):
        self.time = reset

    def get_size(self):
        return self.x - 24, self.y - 24, self.x + 24, self.y + 24

    def draw_box(self):
        draw_rectangle(*self.get_size ())

    def update(self, frame_time):
        self.time += frame_time*10
        distance = Enemy.Enemy_SPEED_PPS * frame_time
        self.y -= distance
        if self.y < 0 :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x,self.y)


class MiddleEnemy(Enemy):
    LEFT_DIR, RIGHT_DIR, GO_STRAIGHT = 0, 1, 2,
    SIZE = 44
    def __init__(self):
        self.x, self.y = random.randint(50, 750), 600
        self.distance = 0
        self.state = random.randint(0, 2)
        self.stateTime = 0
        self.time = 0
        MiddleEnemy.image = load_image('image/enemy/MiddleEnemy.png')

    def handle_LeftDir(self):
        self.x -= self.distance
        self.y -= self.distance
        self.state = self.LEFT_DIR
        if self.x < 0:
            self.state = self.RIGHT_DIR
            self.x = 0
        if self.stateTime > 3:
            self.state = self.GO_STRAIGHT
            self.stateTime = 0

    def handle_RightDir(self):
        self.x += self.distance
        self.y -= self.distance
        self.state = self.RIGHT_DIR
        if self.x > 800:
            self.state = self.LEFT_DIR
            self.x = 800
        if self.stateTime > 3:
            self.state = self.GO_STRAIGHT
            self.stateTime = 0

    def handle_GoStraight(self):
        self.y -= self.distance
        self.state = self.GO_STRAIGHT
        if self.stateTime > 3:
            self.state = random.randint(0, 2)
            self.stateTime = 0

    handle_state = {
        LEFT_DIR: handle_LeftDir,
        RIGHT_DIR: handle_RightDir,
        GO_STRAIGHT: handle_GoStraight
    }

    def update(self, frame_time):
        self.stateTime += frame_time * 10
        self.time += frame_time * 10
        self.distance = Enemy.Enemy_SPEED_PPS * frame_time
        self.handle_state[self.state](self)
        if self.y < 0 :
            return True
        else :
            return False

    def draw(self):
        self.image.clip_draw(self.state * self.SIZE, 0
                             , self.SIZE, 64, self.x, self.y)
