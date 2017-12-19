import json
import os
from pico2d import *

from BackGround import *
from Player import Player   # import Player class from Player.py
from Missile import *
from Enemy import *
from Explosion import *
from Score import *
from Item import *
import Game_FrameWork
import logo_state
import pause_state

name = "FirstStageState"

StageTime = 0        # 게임 시작
score = None
background = None
player = None


explosion = None
# List
PLAYER_MISSILES = None

ENEMY_LIST = None
MiddleEnemyList = None
ENEMY_MISSILE_LIST = None
ExplosionList = None

isBullet_On = False
enemyCreateTime = 0
midEnemyCreateTime = 0
missileCreateTime = 0

# Item
PowerItemList = None
PowerItemTime = 0
BombItemList = None
BombItemTime = 0

def init_object():
    global background, player, score, PowerItemList, BombItemList
    global PLAYER_MISSILES
    global ENEMY_LIST, ENEMY_MISSILE_LIST, ExplosionList, MiddleEnemyList

    background = BackGround()
    score = Score()
    player = Player()

    PLAYER_MISSILES = []

    ENEMY_LIST = []
    ENEMY_MISSILE_LIST = []
    ExplosionList = []
    MiddleEnemyList = []

    PowerItemList = []
    BombItemList = []


def enter():
    Game_FrameWork.reset_time()
    init_object()


def exit():
    global StageTime, background, score, player
    global PLAYER_MISSILES
    global ENEMY_LIST, ENEMY_MISSILE_LIST, ExplosionList, MiddleEnemyList

    del background
    del score
    del player

    del PLAYER_MISSILES

    del ENEMY_LIST
    del ENEMY_MISSILE_LIST
    del ExplosionList
    del MiddleEnemyList

    StageTime = 0

def update(frame_time):
    global StageTime
    global isBullet_On, enemy_missile, enemy, explosion
    global missileCreateTime, PowerItemList

    # createUpdate---------------------------------
    createEnemy(frame_time)
    createItem(frame_time)
    # ---------------------------------------------
    missileCreateTime += frame_time * 10

    player.update(frame_time)
    if player.get_HP() > 0:
        StageTime += frame_time
        score.setTime(StageTime)
        if isBullet_On and missileCreateTime > 2:
            if player.upgrade_missile :
                player_missile = Missile(*player.get_pos())
                PLAYER_MISSILES.append(player_missile)
                missileCreateTime = 0
            else :
                straight_missile = SpecialMissile(player.x,player.y,0)
                left_missile = SpecialMissile(player.x,player.y,1)
                right_missile = SpecialMissile(player.x, player.y, 2)
                straight_missile.specialSound.play(3)
                PLAYER_MISSILES.append(straight_missile)
                PLAYER_MISSILES.append(left_missile)
                PLAYER_MISSILES.append(right_missile)
                missileCreateTime = 0


    background.update(frame_time)
    missileObjects(frame_time)
    itemObjects(frame_time)

    # collision
    for object in PLAYER_MISSILES :
        for enemise in ENEMY_LIST :
            if collision(object,enemise) :
                PLAYER_MISSILES.remove(object)
                explosion = EnemyExplosion(enemise.x,enemise.y)
                ExplosionList.append(explosion)
                ENEMY_LIST.remove(enemise)
                score.setScore(5)
    for object in PLAYER_MISSILES:
        for enemise in MiddleEnemyList :
            if collision(object,enemise) :
                PLAYER_MISSILES.remove(object)
                explosion = EnemyExplosion(enemise.x,enemise.y)
                ExplosionList.append(explosion)
                MiddleEnemyList.remove(enemise)
                score.setScore(10)

    for missileIter in ENEMY_MISSILE_LIST:
        if collision(missileIter,player) :
            ENEMY_MISSILE_LIST.remove(missileIter)
            if player.get_HP() > 0 :
                player.set_damage(10)

    for explosions in ExplosionList :
        isDel = explosions.update(frame_time)
        if isDel == True:
            ExplosionList.remove(explosions)

    for poweritem in PowerItemList:
        if collision(poweritem,player) :
            poweritem.itemSound.play()
            PowerItemList.remove(poweritem)
            player.change_Missile()

    for bombitem in BombItemList:
        if collision(bombitem,player) :
            bombitem.itemSound.play()
            BombItemList.remove(bombitem)
            player.set_bombItem(1)

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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            if player.get_HP() <=0:
                 player.revive()
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
            ENEMY_LIST.append(enemy1)
            ENEMY_LIST.append(enemy2)
            enemyCreateTime = 0.0
    else:
        if enemyCreateTime >= 2.0:
            enemy = Enemy()
            ENEMY_LIST.append(enemy)
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


def createItem(frame_time):
    global PowerItemTime, BombItemTime
    PowerItemTime += frame_time
    BombItemTime += frame_time

    if PowerItemTime > 3 :
        item = PowerItem()
        PowerItemList.append(item)
        PowerItemTime = 0

    if BombItemTime > 3 :
        item = BombItem()
        BombItemList.append(item)
        BombItemTime = 0


def missileObjects(frame_time):
    for object in PLAYER_MISSILES:
        isDel = object.update(frame_time)
        if isDel == True:
            PLAYER_MISSILES.remove(object)

    for object in ENEMY_LIST :
        isDel = object.update(frame_time)
        if object.getMissileTime() > 8:
            enemy_missile = EnummyMissile(*object.get_pos())
            ENEMY_MISSILE_LIST.append(enemy_missile)
            object.setMissileTime(0)
        if isDel == True:
            ENEMY_LIST.remove(object)

    for object in MiddleEnemyList :
        isDel = object.update(frame_time)
        if object.getMissileTime() > 5:
            enemy_missile = EnummyMissile(*object.get_pos())
            ENEMY_MISSILE_LIST.append(enemy_missile)
            object.setMissileTime(0)
        if isDel == True:
            MiddleEnemyList.remove(object)

    for object in ENEMY_MISSILE_LIST :
        isDel = object.update(frame_time)
        if isDel == True :
            ENEMY_MISSILE_LIST.remove(object)


def itemObjects(frame_time):
    for object in PowerItemList :
        isDel = object.update(frame_time)

        if isDel == True:
            PowerItemList.remove(object)

    for object in BombItemList:
        isDel = object.update(frame_time)

        if isDel == True:
            BombItemList.remove(object)


def collision(a, b):
    left_a, bottom_a, right_a, top_a = a.get_size()
    left_b, bottom_b, right_b, top_b = b.get_size()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True


def draw_stage_scene():
    background.draw()

    for enemise in ENEMY_LIST :
        enemise.draw()
        enemise.draw_box()

    for enemise in MiddleEnemyList :
        enemise.draw()
        enemise.draw_box()

    for e_bullet in ENEMY_MISSILE_LIST :
        e_bullet.draw()
        e_bullet.draw_box()

    for explosions in ExplosionList :
        explosions.draw()

    for powerItem in PowerItemList :
        powerItem.draw()

    for bombItem in BombItemList :
        bombItem.draw()

    player.draw()
    player.draw_box()

    for player_missile in PLAYER_MISSILES:
        player_missile.draw()
        player_missile.draw_box()


def draw(frame_time):
    clear_canvas()
    draw_stage_scene()
    score.draw()
    update_canvas()


def pause():
    pass


def resume():
    pass
