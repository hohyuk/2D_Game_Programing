import math
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
    missileSound = None

    def __init__(self, x, y):
        self.x, self.y = x, y

        Missile.image = load_image('image/missile/Missile.png')

        if Missile.missileSound == None:
            Missile.missileSound = load_wav('sound/Missile.wav')
            Missile.missileSound.set_volume(90)

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


class SpecialMissile(Missile):
    SPECIAL_SIZEX = 40
    SPECIAL_SIZEY = 48
    STRAIGHT_MISSILE, LEFT_MISSILE, RIGHT_MISSILE = 0, 1, 2
    specialSound = None

    def __init__(self, x, y, dir):
        self.x, self.y = x, y
        self.dir = dir
        Missile.image = load_image('image/missile/Special_Bullet.png')
        if SpecialMissile.specialSound == None:
            SpecialMissile.specialSound = load_wav('sound/Missile.wav')
            SpecialMissile.specialSound.set_volume(64)

    def update(self, frame_time):
        bullet_distance = Missile.MISSILE_SPEED_PPS * frame_time

        if self.dir == SpecialMissile.LEFT_MISSILE :
            self.x-= bullet_distance
        elif self.dir == SpecialMissile.RIGHT_MISSILE :
            self.x += bullet_distance

        self.y += bullet_distance
        if self.y > 600 :
            return True
        else :
            return False

    def draw(self):
        self.image.clip_draw(SpecialMissile.SPECIAL_SIZEX * self.dir, 0
                                 , SpecialMissile.SPECIAL_SIZEX, SpecialMissile.SPECIAL_SIZEY, self.x, self.y)


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


class MagicMissile(Missile):
    MISSILE_SIZE = 38

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.state = 0
        MagicMissile.image = load_image('image/missile/Magic_Missile.png')
        MagicMissile.time = 0

    def update(self, frame_time):
        self.state = (self.state + 1) % 3
        enemy_missile_distance = Missile.MISSILE_SPEED_PPS * frame_time
        self.y -= enemy_missile_distance
        if self.y < 0 :
            return True
        else :
            return False

    def draw(self):
        self.image.clip_draw(self.state * self.MISSILE_SIZE, 0
                             , self.MISSILE_SIZE, self.MISSILE_SIZE, self.x, self.y)

    def get_size(self):
        return self.x - self.MISSILE_SIZE/2, self.y - self.MISSILE_SIZE/2, self.x + self.MISSILE_SIZE/2, \
               self.y + self.MISSILE_SIZE/2

    def draw_box(self):
        draw_rectangle(*self.get_size())


class RotateMissile:
    MISSILE_HALF_SIZE_X = 10
    MISSILE_HALF_SIZE_Y = 15
    PIXEL_PER_METER = (10.0 / 1.5)  # 10 pixel 1.5m
    MISSILE_SPEED_KMPH = 500.0  # 약 500km
    MISSILE_SPEED_MPM = (MISSILE_SPEED_KMPH * 1000.0 / 60.0)
    MISSILE_SPEED_MPS = (MISSILE_SPEED_MPM / 60.0)
    MISSILE_SPEED_PPS = (MISSILE_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self, posx, posy, rad):
        self.posX, self.posY =posx, posy
        self.x, self.y = 0, 0
        self.rad = rad * 10
        self.speed = 1
        self.distance = 0
        RotateMissile.image = load_image('image/missile/Missile_Enemy01.png')
        RotateMissile.time = 0

    def update(self, frame_time):
        rotate_missile_distance = RotateMissile.MISSILE_SPEED_PPS * frame_time
        self.distance += self.speed

        self.x = self.posX + math.cos(self.rad * math.pi / 180) * self.distance
        self.y = self.posY + math.sin(self.rad * math.pi / 180) * self.distance
        if self.distance > 600:
            return True
        else:
            return False

    def get_size(self):
        return self.x - self.MISSILE_HALF_SIZE_X, self.y - self.MISSILE_HALF_SIZE_Y, self.x + \
               self.MISSILE_HALF_SIZE_X, self.y + self.MISSILE_HALF_SIZE_Y

    def draw_box(self):
        draw_rectangle(*self.get_size())

    def draw(self):
        self.image.draw(self.x, self.y)
