
from pico2d import *
import Game_FrameWork


class Bullet:
    BULLET_SPEED = 600
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y

        Bullet.image = load_image('image/bullet/Bullet.png')

    def update(self, frame_time):
        bullet_distance = Bullet.BULLET_SPEED * frame_time
        self.y += bullet_distance
        if self.y > 500 :
            return True
        else :
            return False

    def get_bb(self):
        return self.x - 15, self.y - 20, self.x + 15, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self):
        self.image.draw(self.x, self.y)


class EnummyBullet(Bullet):
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y

        EnummyBullet.image = load_image('image/bullet/Bullet_Enemy01.png')

    def update(self, frame_time):
        enemy_bullet_distance = Bullet.BULLET_SPEED * frame_time
        self.y -= enemy_bullet_distance
        if self.y < 50 :
            return True
        else :
            return False

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
