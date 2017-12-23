import random
from pico2d import *

import Game_FrameWork

from Explosion import BossExplosion

class Boss:
    SIZEX = 400
    SIZEY = 309

    PIXEL_PER_METER = (10.0 / 22.25)  # 10 pixel 22.25m -> 22.25cm -> 73fit
    Boss_SPEED_KMPH = 1500.0  # 2마하 -> 약 2000km
    Boss_SPEED_MPM = (Boss_SPEED_KMPH * 1000.0 / 60.0)
    Boss_SPEED_MPS = (Boss_SPEED_MPM / 60.0)
    Boss_SPEED_PPS = (Boss_SPEED_MPS * PIXEL_PER_METER)
    image = None
    weakImage = None

    STOP_DIR, LEFT_DIR, RIGHT_DIR  = 0, 1, 2

    def __init__(self):
        self.x, self.y = 400, 800
        self.HP = 500
        self.stateTime = 0
        self.moveTime = 0
        self.Time = 0
        self.state =0
        self.dir = 0
        self.distance = 0
        self.specialAttack = False
        self.Explosion = None
        self.isDie = False
        Boss.image = load_image('image/boss/Boss01.png')
        Boss.weakImage = load_image('image/boss/Boss02.png')

    def handle_StopDir(self):
        self.specialAttack = True
        if self.moveTime > 3:
            self.specialAttack = False
            self.dir = random.randint(1, 2)
            self.moveTime = 0

    def handle_LeftDir(self):
        self.x -= self.distance
        if self.x < 0 + self.SIZEX / 2:
            self.state = self.RIGHT_DIR
            self.x = 0 + self.SIZEX / 2
        if self.moveTime > 3:
            self.dir = self.STOP_DIR
            self.moveTime = 0

    def handle_RightDir(self):
        self.x += self.distance
        if self.x > 800 - self.SIZEX / 2:
            self.dir = self.LEFT_DIR
            self.x = 800 - self.SIZEX / 2
        if self.moveTime > 3:
            self.dir = self.STOP_DIR
            self.moveTime = 0

    handle_state = {
        STOP_DIR: handle_StopDir,
        LEFT_DIR: handle_LeftDir,
        RIGHT_DIR: handle_RightDir
    }

    def update(self, frame_time):
        if self.HP > 0:
            self.stateTime += frame_time
            self.moveTime += frame_time
            self.Time += frame_time
            self.distance = Boss.Boss_SPEED_PPS * frame_time
            if self.y > 450:
                self.y -= self.distance
            else:
                self.handle_state[self.dir](self)

            if self.stateTime > 0.5:
                self.state = (self.state + 1) % 4
                self.stateTime = 0
        else:
            if self.Explosion == None:
                self.Explosion = BossExplosion(self.x,self.y)
            else:
                self.Explosion.update(frame_time)

    def draw(self):
        if self.HP > 100 :
            self.image.clip_draw(self.state * self.SIZEX, 0
                                 , self.SIZEX, self.SIZEY, self.x, self.y)
        elif self.HP > 0:
            self.weakImage.clip_draw(self.state * self.SIZEX, 0
                                     , self.SIZEX, self.SIZEY, self.x, self.y)
        elif self.Explosion != None:
            if self.Explosion.state < 4:
                self.Explosion.draw()
            else:
                self.isDie = True

    def draw_box(self):
        draw_rectangle(*self.get_size())

    def get_size(self):
        return self.x - self.SIZEX/4, self.y - self.SIZEY/2, self.x + self.SIZEX/4, self.y + self.SIZEY/2

    def set_damage(self, damage):
        self.HP -= damage

    def get_left_pos(self):
        return self.x - 80, self.y - 30

    def get_right_pos(self):
        return self.x + 80, self.y - 30