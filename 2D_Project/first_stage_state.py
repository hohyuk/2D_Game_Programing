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
enemy_bullet = None

# List
PLAYER_BULLETS = None
ENEMiES = None
ENEMY_BULLETS = None

isBullet_On = False
bulletTime = 0
e_bulletTime = 0

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
        self.image2 = load_image('image\stage\stage1_02.png')
        self.image3 = load_image('image\stage\stage1_03.png')
        self.width = Game_FrameWork.Width
        self.height = 6000

        self.x1, self.y1 = self.width / 2, self.height / 2           # 화면 초기값. stage1_01 초기값.
        self.x2, self.y2 = self.width / 2, self.height / 2 + 600     # stage1_02화면 초기값.
        self.x3, self.y3 = self.width / 2, self.height / 2 + 600     # stage1_02화면 초기값.
        self.move = 0.2

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
#-----------------------------------------------------------------------------------------------------------


def create_object():
    global my_timer,background, player
    global PLAYER_BULLETS, ENEMiES, ENEMY_BULLETS

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
    global PLAYER_BULLETS, ENEMiES, ENEMY_BULLETS

    del my_timer
    del background
    del player

    del PLAYER_BULLETS
    del ENEMiES
    del ENEMY_BULLETS


def update(frame_time):
    global my_timer, player_bullet, isBullet_On, enemy_bullet
    global bulletTime, e_bulletTime

    bulletTime += frame_time * 10
    e_bulletTime += frame_time * 10

    if isBullet_On and bulletTime > 2:
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
        isDel = enemise.update(frame_time)
        if e_bulletTime > 4:
            enemy_bullet = EnummyBullet(*enemise.get_pos())
            ENEMY_BULLETS.append(enemy_bullet)
            e_bulletTime = 0
        if isDel == True:
            ENEMiES.remove(enemise)

    for e_bullet in ENEMY_BULLETS :
        isDel = e_bullet.update(frame_time)
        if isDel == True :
            ENEMY_BULLETS.remove(e_bullet)

    # collision
    for p_bullet in PLAYER_BULLETS :
        for enemise in ENEMiES :
            if collision(p_bullet,enemise) :
                PLAYER_BULLETS.remove(p_bullet)
                ENEMiES.remove(enemise)
def draw_stage_scene():
    background.draw()
    player.draw()
    player.draw_bb()
    for p_bullet in PLAYER_BULLETS :
        p_bullet.draw()
        p_bullet.draw_bb()

    for enemise in ENEMiES :
        enemise.draw()
        enemise.draw_bb()

    for e_bullet in ENEMY_BULLETS :
        e_bullet.draw()
        e_bullet.draw_bb()


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


def collision(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True


def pause():
    pass


def resume():
    pass
