
from pico2d import *
import Game_FrameWork


class Missile:
    MISSILE_HALF_SIZE_X = 10
    MISSILE_HALF_SIZE_Y = 15
    PIXEL_PER_METER = (10.0 / 1.5)       # 10 pixel 1.5m
    MISSILE_SPEED_KMPH = 500.0          # 약 500km
    MISSILE_SPEED_MPM = (MISSILE_SPEED_KMPH * 1000.0 / 60.0)
    MISSILE_SPEED_MPS = (MISSILE_SPEED_MPM / 60.0)
    MISSILE_SPEED_PPS = (MISSILE_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y

        Missile.image = load_image('image/missile/Missile.png')

    def update(self, frame_time):
        bullet_distance = Missile.MISSILE_SPEED_PPS * frame_time
        self.y += bullet_distance
        if self.y > 600 :
            return True
        else :
            return False

    def get_size(self):
        return self.x - self.MISSILE_HALF_SIZE_X, self.y - self.MISSILE_HALF_SIZE_Y, self.x + self.MISSILE_HALF_SIZE_X, self.y + self.MISSILE_HALF_SIZE_Y

    def draw_box(self):
        draw_rectangle(*self.get_size())

    def draw(self):
        self.image.draw(self.x, self.y)


class EnummyMissile(Missile):
    MISSILE_HALF_SIZE_X = 10
    MISSILE_HALF_SIZE_Y = 10


    def __init__(self, x, y):
        self.x, self.y = x, y
        EnummyMissile.image = load_image('image/missile/Missile_Enemy01.png')
        EnummyMissile.time = 0

    def update(self, frame_time):
        enemy_missile_distance = Missile.MISSILE_SPEED_PPS * frame_time
        self.y -= enemy_missile_distance
        if self.y < 0 :
            return True
        else :
            return False

    def get_size(self):
        return self.x - self.MISSILE_HALF_SIZE_X, self.y - self.MISSILE_HALF_SIZE_Y, self.x + self.MISSILE_HALF_SIZE_X, self.y + self.MISSILE_HALF_SIZE_Y

    def draw_box(self):
        draw_rectangle(*self.get_size())
