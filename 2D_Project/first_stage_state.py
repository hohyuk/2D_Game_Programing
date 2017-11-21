import json
import os
from pico2d import *

from Player import Player   # import Player class from Player.py
from Bullet import Bullet

import Game_FrameWork
import pause_state



name = "FirstStageState"


background = None
player = None
player_bullet = None

# List
PLAYER_BULLETS = None

isBullet_On = False
bulletTime = 0
class BackGround:
    def __init__(self):
        self.image1 = load_image('image\stage\stage1_01.png')
        self.image2 = load_image('image\stage\stage1_02.png')
        self.image3 = load_image('image\stage\stage1_03.png')
        self.width = Game_FrameWork.Width
        self.height = 6000

        self.x1, self.y1 = self.width / 2, self.height / 2           # 화면 초기값. stage1_01 초기값.
        self.x2, self.y2 = self.width / 2, self.height / 2 + 600     # stage1_02화면 초기값.
        self.x3, self.y3 = self.width / 2, self.height / 2 + 600     # stage1_02화면 초기값.
        self.move = 0.5

    def update(self, frame_time):
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


def create_object():
    global background, player
    global PLAYER_BULLETS

    background = BackGround()
    player = Player()
    PLAYER_BULLETS = []


def enter():
    Game_FrameWork.reset_time()
    create_object()


def exit():
    global background, player
    global PLAYER_BULLETS
    del background
    del player

    del PLAYER_BULLETS


def update(frame_time):
    global player_bullet, isBullet_On, bulletTime
    bulletTime += frame_time * 10
    if isBullet_On and bulletTime > 0.5:
        player_bullet = Bullet(*player.get_pos())
        PLAYER_BULLETS.append(player_bullet)
        bulletTime = 0


    background.update(frame_time)
    player.update(frame_time)

    for p_bullet in PLAYER_BULLETS :
        isDel = p_bullet.update(frame_time)
        if isDel == True :
            PLAYER_BULLETS.remove(p_bullet)


def draw_stage_scene():
    background.draw()
    player.draw()

    for p_bullet in PLAYER_BULLETS :
        p_bullet.draw()


def draw(frame_time):
    clear_canvas()
    draw_stage_scene()
    update_canvas()


def handle_events(frame_time):
    global player, isBullet_On
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            Game_FrameWork.push_state(pause_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                isBullet_On = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
            isBullet_On = False
        else:
            player.handle_event(event)


def pause():
    pass


def resume():
    pass


# bullet

