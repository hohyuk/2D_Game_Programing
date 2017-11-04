import json
import os
from pico2d import *

import Game_FrameWork


name = "FirstStageState"


background = None


class BackGround:
    def __init__(self):
        self.image = load_image('image\stage\stage1_01.png')
        self.width = 800
        self.height = 6000
        self.x, self.y= self.width / 2, self.height / 2            # 화면 초기값.
        self.move = 0.5

    def update(self):
        if self.y > -(self.height / 2):
            self.y -= self.move

    def draw(self):
        self.image.clip_draw(0, 0, self.width, self.height, self.x, self.y)


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