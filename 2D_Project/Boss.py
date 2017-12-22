from pico2d import *

import Game_FrameWork


class Boss:
    SIZEX = 400
    SIZEY = 309

    PIXEL_PER_METER = (10.0 / 22.25)  # 10 pixel 22.25m -> 22.25cm -> 73fit
    Boss_SPEED_KMPH = 1500.0  # 2마하 -> 약 2000km
    Boss_SPEED_MPM = (Boss_SPEED_KMPH * 1000.0 / 60.0)
    Boss_SPEED_MPS = (Boss_SPEED_MPM / 60.0)
    Boss_SPEED_PPS = (Boss_SPEED_MPS * PIXEL_PER_METER)
    image = None

    def __init__(self):
        self.x, self.y = 400, 800
        self.statetime = 0
        self.state =0
        Boss.image = load_image('image/boss/Boss01.png')

    def update(self, frame_time):
        self.statetime += frame_time

        if self.statetime > 0.5:
            self.state = (self.state + 1) % 4
            self.statetime = 0

        if self.y > 450 :
            distance = Boss.Boss_SPEED_PPS * frame_time
            self.y -= distance



    def draw(self):
        self.image.clip_draw(self.state * self.SIZEX, 0
                             , self.SIZEX, self.SIZEY, self.x, self.y)