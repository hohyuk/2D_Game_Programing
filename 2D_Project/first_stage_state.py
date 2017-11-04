import json
import os
from pico2d import *

import Game_FrameWork


name = "FirstStageState"


background = None


class BackGround:
    def __init__(self):
        self.image = load_image('image\stage\Stage1_01.png')

    def draw(self):
        self.image.clip_draw(0, 0, 800,600,400,300)


def enter():
    global background
    background = BackGround()


def exit():
    global background
    del background


def update():
    pass


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