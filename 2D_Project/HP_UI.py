from pico2d import *

import Game_FrameWork


class PlayerHpBar:
    image = None

    def __init__(self):
        self.x = 100
        self.y = 580
        PlayerHpBar.image = load_image('image/player/HpBar.png')

    def draw(self):
        self.image.draw(self.x, self.y)


class PlayerHpGauge:
    image = None

    def __init__(self):
        self.width = 180
        self.height = 10
        self.x = 10
        self.y = 575

        PlayerHpGauge.image = load_image('image/player/HpGauge.png')

    def draw(self,hp):
        self.image.clip_draw_to_origin(0, 0, self.width, self.height, self.x, self.y, hp,10)


class BoomUI:
    image = None
    def __init__(self):
        self.width = 300
        self.height = 50
        self.x = 0 # 위치
        self.y = 0

        BoomUI.image = load_image('image/item/BoomUI.png')

    def draw(self,addBoom):
        addBoom *= 60
        if addBoom >= 300:
            addBoom = 300

        self.image.clip_draw_to_origin(0, 0, addBoom, self.height, \
                                       self.x, self.y, addBoom, (self.height-10))