import json
import os
from pico2d import *

from BackGround import *
from Player import Player   # import Player class from Player.py
from Missile import *
from Enemy import *
from Explosion import *
from Score import *
import Game_FrameWork
import logo_state
import pause_state

name = "FirstStageState"

StageTime = 0        # 게임 시작
score = None
background = None
player = None
player_missile = None

enemy = None
enemy_missile = None
explosion = None
# List
PLAYER_MISSILES = None
ENEMiES = None
MiddleEnemyList = None
ENEMY_MISSILES = None
ExplosionList = None

isBullet_On = False
enemyCreateTime = 0
midEnemyCreateTime = 0
missileCreateTime = 0


def create_object():
    global background, player, score
    global PLAYER_MISSILES, ENEMiES, ENEMY_MISSILES, ExplosionList, MiddleEnemyList

    background = BackGround()
    score = Score()
    player = Player()

    PLAYER_MISSILES = []
    ENEMiES = []
    ENEMY_MISSILES = []
    ExplosionList = []
    MiddleEnemyList = []

def enter():
    Game_FrameWork.reset_time()
    create_object()


def exit():
    global StageTime, background, score, player
    global PLAYER_MISSILES, ENEMiES, ENEMY_MISSILES, ExplosionList

    del background
    del score
    del player

    del PLAYER_MISSILES
    del ENEMiES
    del ENEMY_MISSILES
    del ExplosionList

    StageTime = 0

def update(frame_time):
    global StageTime
    global player_missile, isBullet_On, enemy_missile, enemy, explosion
    global missileCreateTime

    StageTime += frame_time

    createEnemy(frame_time)

    missileCreateTime += frame_time * 10

    player.update(frame_time)
    if player.get_HP() > 0:
        score.setTime(StageTime)
        if isBullet_On and missileCreateTime > 2:
            player_missile = Missile(*player.get_pos())
            PLAYER_MISSILES.append(player_missile)
            missileCreateTime = 0

    background.update(frame_time)
    createObjects(frame_time)

    # collision
    for object in PLAYER_MISSILES :
        for enemise in ENEMiES :
            if collision(object,enemise) :
                PLAYER_MISSILES.remove(object)
                explosion = EnemyExplosion(enemise.x,enemise.y)
                ExplosionList.append(explosion)
                ENEMiES.remove(enemise)
                score.setScore(5)
    for object in PLAYER_MISSILES:
        for enemise in MiddleEnemyList :
            if collision(object,enemise) :
                PLAYER_MISSILES.remove(object)
                explosion = EnemyExplosion(enemise.x,enemise.y)
                ExplosionList.append(explosion)
                MiddleEnemyList.remove(enemise)
                score.setScore(10)

    for missileIter in ENEMY_MISSILES:
        if collision(missileIter,player) :
            ENEMY_MISSILES.remove(missileIter)
            if player.get_HP() > 0 :
                player.set_damage(10)

    for explosions in ExplosionList :
        isDel = explosions.update(frame_time)
        if isDel == True:
            ExplosionList.remove(explosions)


def draw_stage_scene():
    background.draw()

    for enemise in ENEMiES :
        enemise.draw()
        enemise.draw_box()

    for enemise in MiddleEnemyList :
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
    score.draw()
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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            if player.get_HP() <=0 :
                Game_FrameWork.change_state(logo_state)
        else:
            player.handle_event(event)


def createEnemy(frame_time):
    global StageTime
    global enemyCreateTime, midEnemyCreateTime

    enemyCreateTime += frame_time
    midEnemyCreateTime += frame_time

    if StageTime >10 :
        if enemyCreateTime >= 2.0:
            enemy1 = Enemy()
            enemy2 = Enemy()
            ENEMiES.append(enemy1)
            ENEMiES.append(enemy2)
            enemyCreateTime = 0.0
    else:
        if enemyCreateTime >= 2.0:
            enemy = Enemy()
            ENEMiES.append(enemy)
            enemyCreateTime = 0.0
    # 20초 후 중간 적이 나온다.
    if StageTime > 25 :
        if midEnemyCreateTime >= 2.0:
            midEnemy1 = MiddleEnemy()
            midEnemy2 = MiddleEnemy()
            MiddleEnemyList.append(midEnemy1)
            MiddleEnemyList.append(midEnemy2)
            midEnemyCreateTime = 0
    elif StageTime > 15 :
        if midEnemyCreateTime >= 2.0:
            midEnemy1 = MiddleEnemy()
            MiddleEnemyList.append(midEnemy1)
            midEnemyCreateTime = 0


def createObjects(frame_time):
    for object in PLAYER_MISSILES :
        isDel = object.update(frame_time)
        if isDel == True :
            PLAYER_MISSILES.remove(object)

    for object in ENEMiES :
        isDel = object.update(frame_time)
        if object.getMissileTime() > 8:
            enemy_missile = EnummyMissile(*object.get_pos())
            ENEMY_MISSILES.append(enemy_missile)
            object.setMissileTime(0)
        if isDel == True:
            ENEMiES.remove(object)

    for object in MiddleEnemyList :
        isDel = object.update(frame_time)
        if object.getMissileTime() > 5:
            enemy_missile = EnummyMissile(*object.get_pos())
            ENEMY_MISSILES.append(enemy_missile)
            object.setMissileTime(0)
        if isDel == True:
            MiddleEnemyList.remove(object)

    for object in ENEMY_MISSILES :
        isDel = object.update(frame_time)
        if isDel == True :
            ENEMY_MISSILES.remove(object)

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
