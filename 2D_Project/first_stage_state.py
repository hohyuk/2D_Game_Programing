import json
import os
from pico2d import *

from BackGround import *
from Player import Player   # import Player class from Player.py
from Missile import *
from Enemy import Enemy
from Explosion import *
import Game_FrameWork
import pause_state

name = "FirstStageState"

background = None
player = None
player_missile = None
enemy = None
enemy_missile = None
explosion = None
# List
PLAYER_MISSILES = None
ENEMiES = None
ENEMY_MISSILES = None
ExplosionList = None

isBullet_On = False
enemyTime = 0
bulletTime = 0
e_bulletTime = 0


def create_object():
    global background, player
    global PLAYER_MISSILES, ENEMiES, ENEMY_MISSILES, ExplosionList

    background = BackGround()
    player = Player()

    PLAYER_MISSILES = []
    ENEMiES = []
    ENEMY_MISSILES = []
    ExplosionList = []


def enter():
    Game_FrameWork.reset_time()
    create_object()


def exit():
    global background, player
    global PLAYER_MISSILES, ENEMiES, ENEMY_MISSILES, ExplosionList

    del background
    del player

    del PLAYER_MISSILES
    del ENEMiES
    del ENEMY_MISSILES
    del ExplosionList

def update(frame_time):
    global player_missile, isBullet_On, enemy_missile, enemyTime, enemy, explosion
    global bulletTime, e_bulletTime

    enemyTime += frame_time
    if enemyTime >= 2.0:
        enemy = Enemy()
        ENEMiES.append(enemy)
        enemyTime = 0.0

    bulletTime += frame_time * 10
    e_bulletTime += frame_time * 10

    if isBullet_On and bulletTime > 2:
        player_missile = Missile(*player.get_pos())
        PLAYER_MISSILES.append(player_missile)
        bulletTime = 0

    background.update(frame_time)
    player.update(frame_time)

    for p_bullet in PLAYER_MISSILES :
        isDel = p_bullet.update(frame_time)
        if isDel == True :
            PLAYER_MISSILES.remove(p_bullet)

    for enemise in ENEMiES :
        isDel = enemise.update(frame_time)
        if e_bulletTime > 4:
            enemy_missile = EnummyMissile(*enemise.get_pos())
            ENEMY_MISSILES.append(enemy_missile)
            e_bulletTime = 0
        if isDel == True:
            ENEMiES.remove(enemise)

    for e_bullet in ENEMY_MISSILES :
        isDel = e_bullet.update(frame_time)
        if isDel == True :
            ENEMY_MISSILES.remove(e_bullet)

    # collision
    for p_bullet in PLAYER_MISSILES :
        for enemise in ENEMiES :
            if collision(p_bullet,enemise) :
                PLAYER_MISSILES.remove(p_bullet)
                explosion = EnemyExplosion(enemise.x,enemise.y)
                ExplosionList.append(explosion)
                ENEMiES.remove(enemise)

    for explosions in ExplosionList :
        isDel = explosions.update(frame_time)
        if isDel == True:
            ExplosionList.remove(explosions)

def draw_stage_scene():
    background.draw()

    for enemise in ENEMiES :
        enemise.draw()
        enemise.draw_box()

    for e_bullet in ENEMY_MISSILES :
        e_bullet.draw()
        e_bullet.draw_box()

    for explosions in ExplosionList :
        explosions.draw()

    player.draw()
    player.draw_box()
    for p_bullet in PLAYER_MISSILES:
        p_bullet.draw()
        p_bullet.draw_box()

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
    left_a, bottom_a, right_a, top_a = a.get_size()
    left_b, bottom_b, right_b, top_b = b.get_size()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True


def pause():
    pass


def resume():
    pass
