
from pico2d import *
import Game_FrameWork


class Bullet:
    BULLET_SPEED = 500
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


        pass

    def get_bb(self):
        return self.x - 24, self.y - 24, self.x + 24, self.y + 24

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self):
        self.image.draw(self.x, self.y)