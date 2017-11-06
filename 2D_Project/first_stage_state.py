import json
import os
from pico2d import *

import Game_FrameWork


name = "FirstStageState"


background = None


class BackGround:
    def __init__(self):
        self.image1 = load_image('image\stage\stage1_01.png')
        self.image2 = load_image('image\stage\stage1_02.png')
        self.image3 = load_image('image\stage\stage1_03.png')
        self.width = 800
        self.height = 6000

        self.x1, self.y1 = self.width / 2, self.height / 2           # 화면 초기값. stage1_01 초기값.
        self.x2, self.y2 = self.width / 2, self.height / 2 + 600

        self.move = 2

    def update(self):
        if self.y1 > -(self.height / 2):
            self.y1 -= self.move
        if self.y1 < -(self.height / 2)+600:
            self.y2 -= self.move


    def draw(self):
        self.image1.clip_draw(0, 0, self.width, self.height, self.x1, self.y1)
        self.image2.clip_draw(0, 0, self.width, self.height, self.x2, self.y2)
        #self.image3.clip_draw(0, 0, self.width, self.height, self.x, self.y)


def enter():
    global background
    background = BackGround()


def exit():
    global background
    del background


def update():
    background.update()


def draw():
    clear_canvas()
    background.draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Game_FrameWork.quit()


def pause():
    pass


def resume():
    pass