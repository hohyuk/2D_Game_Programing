import json
import os
from pico2d import *

import Game_FrameWork
import pause_state

name = "FirstStageState"


background = None
player = None


class BackGround:
    def __init__(self):
        self.image1 = load_image('image\stage\stage1_01.png')
        self.image2 = load_image('image\stage\stage1_02.png')
        self.image3 = load_image('image\stage\stage1_03.png')
        self.width = 800
        self.height = 6000

        self.x1, self.y1 = self.width / 2, self.height / 2           # 화면 초기값. stage1_01 초기값.
        self.x2, self.y2 = self.width / 2, self.height / 2 + 600     # stage1_02화면 초기값.
        self.x3, self.y3 = self.width / 2, self.height / 2 + 600     # stage1_02화면 초기값.
        self.move = 0.5

    def update(self):
        if self.y1 > -(self.height / 2):
            self.y1 -= self.move
        if self.y1 < -(self.height / 2)+600:
            self.y2 -= self.move
        if (self.y2 < -(self.height / 2) + 600) and (self.y3 > -(self.height / 2) + 600):
            self.y3 -= self.move

    def draw(self):
        self.image1.clip_draw(0, 0, self.width, self.height, self.x1, self.y1)
        self.image2.clip_draw(0, 0, self.width, self.height, self.x2, self.y2)
        self.image3.clip_draw(0, 0, self.width, self.height, self.x3, self.y3)


class Player:
    STAND, FORWARD, RIGHT, LEFT = 0, 1, 2, 3

    def __init__(self):
        self.image = load_image('image\player\player.png')
        self.frame = 0
        self.state = self.STAND
        self.x, self.y = 400, 90

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.STAND, self.LEFT, self.RIGHT):
                self.state = self.FORWARD
        pass

    def update(self):
        self.frame = (self.frame + 1) % 3
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64,self.x, self.y)


def enter():
    global background, player
    background = BackGround()
    player = Player()


def exit():
    global background, player
    del background
    del player


def update():
    background.update()
    player.update()


def draw_stage_scene():
    background.draw()
    player.draw()


def draw():
    clear_canvas()
    draw_stage_scene()
    update_canvas()


def handle_events():
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Game_FrameWork.push_state(pause_state)
        else:
            player.handle_event(event)


def pause():
    pass


def resume():
    pass

