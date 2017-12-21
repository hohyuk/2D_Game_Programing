import random

from pico2d import *

import Game_FrameWork


class BombAirplan:
    PIXEL_PER_METER = (40.0 / 22.25)  # 40 pixel 22.25m -> 22.25cm -> 73fit
    FLY_SPEED_KMPH = 500.0  # 2마하 -> 약 2400km
    FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
    FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
    FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

    image = None
    bombSound = None
    def __init__(self):
        self.x, self.y = 400, -150

        BombAirplan.image = load_image('image/bomb_airplan/Bomb_Airplan.png')

        if BombAirplan.bombSound == None:
            BombAirplan.bombSound = load_wav('sound/Bomb.wav')
            BombAirplan.bombSound.set_volume(64)

    def update(self, frame_time):
        BombAirplan.bombSound.play()
        distance = BombAirplan.FLY_SPEED_PPS * frame_time
        self.y += distance

        if self.y > 600:
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x,self.y)

    def get_size(self):
        return self.x - 400, self.y -150 , self.x + 400, self.y + 150

    def draw_box(self):
        draw_rectangle(*self.get_size ())
