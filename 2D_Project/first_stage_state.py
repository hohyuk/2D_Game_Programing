import json
import os
from pico2d import *

from Player import Player   # import Player class from Player.py
from Bullet import Bullet, EnummyBullet
from Enemy import Enemy

import Game_FrameWork
import pause_state



name = "FirstStageState"

my_timer = None
background = None
player = None
player_bullet = None
enemy = None
enumy_bullet = None

# List
PLAYER_BULLETS = None
ENEMiES = None
ENEMY_BULLETS = None

isBullet_On = False
bulletTime = 0


#-----------------------------------------------------------------------------------------------------------
class Timer:
    def __init__(self):
        self.time = 0.0
        self.timer = 0.0
        self.min = 0.0
        self.sec = 0.0

    def create_enemy(self):
        global enemy
        if self.time >= 2.0 :
            enemy = Enemy()
            ENEMiES.append(enemy)
            self.time = 0.0

    def update(self,frame_time):
        self.timer += frame_time
        self.time += frame_time
        self.min = int(self.timer / 60)
        self.sec = int(self.timer % 60)
        self.create_enemy()
#-----------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------
class BackGround:
    def __init__(self):
        self.image1 = load_image('image\stage\stage1_01.png')
        #self.image2 = load_image('image\stage\stage1_02.png')
        #self.image3 = load_image('image\stage\stage1_03.png')
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
        #self.image2.clip_draw(0, 0, self.width, self.height, self.x2, self.y2)
        #self.image3.clip_draw(0, 0, self.width, self.height, self.x3, self.y3)
#-----------------------------------------------------------------------------------------------------------


def create_object():
    global my_timer,background, player
    global PLAYER_BULLETS, ENEMiES, EnummyBullet

    my_timer = Timer()
    background = BackGround()
    player = Player()

    PLAYER_BULLETS = []
    ENEMiES = []
    ENEMY_BULLETS = []


def enter():
    Game_FrameWork.reset_time()
    create_object()


def exit():
    global background, player, my_timer
    global PLAYER_BULLETS, ENEMiES, EnummyBullet

    del my_timer
    del background
    del player

    del PLAYER_BULLETS
    del ENEMiES
    del EnummyBullet


def update(frame_time):
    global my_timer, player_bullet, isBullet_On, bulletTime,enumy_bullet
    bulletTime += frame_time * 10
    if isBullet_On and bulletTime > 0.5:
        player_bullet = Bullet(*player.get_pos())
        PLAYER_BULLETS.append(player_bullet)
        bulletTime = 0

    my_timer.update(frame_time)
    background.update(frame_time)
    player.update(frame_time)


    for p_bullet in PLAYER_BULLETS :
        isDel = p_bullet.update(frame_time)
        if isDel == True :
            PLAYER_BULLETS.remove(p_bullet)

    for enemise in ENEMiES :
        enemise.update(frame_time)



def draw_stage_scene():
    background.draw()
    player.draw()

    for p_bullet in PLAYER_BULLETS :
        p_bullet.draw()

    for enemise in ENEMiES :
        enemise.draw()


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

