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
from BombAirplan import *
from Boss import *

import Game_FrameWork
import logo_state
import pause_state
import Game_Over_state
import Finish
name = "FirstStageState"

StageTime = 0        # 게임 시작
score = None
background = None
player = None
boss = None
BossCreateTime = 40  # 보스 생성 시간
BossCreate = False  # True면 보스 생성

# List
PLAYER_MISSILES = None

LowEnemyList = None
MiddleEnemyList = None
ENEMY_MISSILE_LIST = None
ExplosionList = None
BigExplosionList = None
HighEnemyList = None

isBullet_On = False
enemyCreateTime = 0
midEnemyCreateTime = 0
highEnemyCreateTime = 0
missileCreateTime = 0

# Item
PowerItemList = None
PowerItemTime = 0
BombItemList = None
BombItemTime = 0

# 필살기
BombAirplanList = None
BombAirplanTime = 0

FINISH = None
def init_object():
    global StageTime, background, player, score, PowerItemList, BombItemList
    global PLAYER_MISSILES, BombAirplanList
    global LowEnemyList, ENEMY_MISSILE_LIST, MiddleEnemyList, HighEnemyList
    global BigExplosionList, ExplosionList, FINISH

    background = BackGround()
    score = Score()
    player = Player()

    PLAYER_MISSILES = []

    LowEnemyList = []
    ENEMY_MISSILE_LIST = []
    ExplosionList = []
    BigExplosionList = []
    MiddleEnemyList = []
    HighEnemyList = []

    PowerItemList = []
    BombItemList = []

    BombAirplanList = []

    StageTime = 0
    FINISH = False

def enter():
    Game_FrameWork.reset_time()
    init_object()


def exit():
    global background, score, player, boss
    global PLAYER_MISSILES, BombAirplanList
    global LowEnemyList, ENEMY_MISSILE_LIST, MiddleEnemyList, HighEnemyList
    global BigExplosionList, ExplosionList

    del background
    del score
    del player

    del PLAYER_MISSILES
    del BombAirplanList

    del LowEnemyList
    del ENEMY_MISSILE_LIST
    del ExplosionList
    del BigExplosionList
    del MiddleEnemyList
    del HighEnemyList
    del boss

def update(frame_time):
    global StageTime, FINISH
    global isBullet_On, enemy_missile, enemy
    global missileCreateTime, PowerItemList
    global BossCreate

    # createUpdate---------------------------------
    createEnemy(frame_time)
    createItem(frame_time)
    # ---------------------------------------------
    missileCreateTime += frame_time * 10

    player.update(frame_time)
    if player.HP > 0:
        StageTime += frame_time
        score.setTime(StageTime)
        if isBullet_On and missileCreateTime > 2:
            if player.upgrade_missile :
                player_missile = Missile(*player.get_pos())
                player_missile.missileSound.play()
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
    elif player.isDie:
        Game_FrameWork.push_state(Game_Over_state)

    if BossCreate :
        if boss.HP <=0 :
            FINISH = True
        if boss.isDie:
            Game_FrameWork.push_state(Finish)
        else:
            boss.update(frame_time)

    background.update(frame_time)
    missileObjects(frame_time)
    itemObjects(frame_time)

    # collision
    for object in PLAYER_MISSILES :
        for enemise in LowEnemyList :
            if collision(object, enemise) :
                PLAYER_MISSILES.remove(object)
                explosion = EnemyExplosion(enemise.x,enemise.y)
                ExplosionList.append(explosion)
                LowEnemyList.remove(enemise)
                score.setScore(5)
    for object in PLAYER_MISSILES:
        for enemise in MiddleEnemyList :
            if collision(object, enemise) :
                PLAYER_MISSILES.remove(object)
                explosion = EnemyExplosion(enemise.x,enemise.y)
                ExplosionList.append(explosion)
                MiddleEnemyList.remove(enemise)
                score.setScore(10)

    for enemise in HighEnemyList:
        for object in PLAYER_MISSILES:
            if collision(object, enemise):
                PLAYER_MISSILES.remove(object)
                explosion = EnemyExplosion(object.x, object.y)
                ExplosionList.append(explosion)
                if enemise.HP >= 0 :
                    enemise.set_damage(10)
                else :
                    score.setScore(30)
                    explosion = BigExplosion(enemise.x, enemise.y)
                    BigExplosionList.append(explosion)
                    HighEnemyList.remove(enemise)
    if BossCreate :
        for object in PLAYER_MISSILES:
            if collision(object, boss):
                PLAYER_MISSILES.remove(object)
                explosion = EnemyExplosion(object.x, object.y)
                ExplosionList.append(explosion)
                if boss.HP >= 0 :
                    boss.set_damage(10)

    for missileIter in ENEMY_MISSILE_LIST:
        if not FINISH :
            if collision(missileIter, player):
                ENEMY_MISSILE_LIST.remove(missileIter)
                if player.HP > 0:
                    player.set_damage(10)


    # 필살기------------------------------------------------------------------
    for bomb in BombAirplanList :
        if collision(bomb, boss):
            explosion = BigExplosion(boss.x, boss.y)
            BigExplosionList.append(explosion)
            boss.set_damage(1)

        for enemise in LowEnemyList :
            if collision(bomb, enemise) :
                explosion = EnemyExplosion(enemise.x,enemise.y)
                ExplosionList.append(explosion)
                LowEnemyList.remove(enemise)
                score.setScore(5)
        for enemise in MiddleEnemyList :
            if collision(bomb, enemise) :
                explosion = EnemyExplosion(enemise.x,enemise.y)
                ExplosionList.append(explosion)
                MiddleEnemyList.remove(enemise)
                score.setScore(10)
        for enemise in HighEnemyList:
            if collision(bomb, enemise):
                explosion = BigExplosion(enemise.x, enemise.y)
                BigExplosionList.append(explosion)
                HighEnemyList.remove(enemise)
                score.setScore(30)
        for missileIter in ENEMY_MISSILE_LIST:
            if collision(bomb, missileIter):
                ENEMY_MISSILE_LIST.remove(missileIter)
                score.setScore(1)
    # ------------------------------------------------------------------------

    for explosions in ExplosionList :
        isDel = explosions.update(frame_time)
        if isDel == True:
            ExplosionList.remove(explosions)

    for explosions in BigExplosionList :
        isDel = explosions.update(frame_time)
        if isDel == True:
            BigExplosionList.remove(explosions)

    for poweritem in PowerItemList:
        if collision(poweritem,player) :
            poweritem.itemSound.play()
            PowerItemList.remove(poweritem)
            player.change_Missile()

    for bombitem in BombItemList:
        if collision(bombitem, player) :
            bombitem.itemSound.play()
            BombItemList.remove(bombitem)
            player.set_bombItem(1)


def createEnemy(frame_time):
    global StageTime
    global enemyCreateTime, midEnemyCreateTime, highEnemyCreateTime
    global boss, BossCreate, BossCreateTime
    enemyCreateTime += frame_time
    midEnemyCreateTime += frame_time
    highEnemyCreateTime += frame_time
    if StageTime >10 :
        if enemyCreateTime >= 2.0:
            enemy1 = Enemy()
            enemy2 = Enemy()
            LowEnemyList.append(enemy1)
            LowEnemyList.append(enemy2)
            enemyCreateTime = 0.0
    else:
        if enemyCreateTime >= 2.0:
            enemy = Enemy()
            LowEnemyList.append(enemy)
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

    if StageTime > 30 :
        if highEnemyCreateTime >= 5.0 :
            highEnemy = HighEnemy()
            HighEnemyList.append(highEnemy)
            highEnemyCreateTime = 0

    if StageTime > BossCreateTime :
        if BossCreate == False :
            boss = Boss()
            background.bgm.stop()
            background.bossBgm.repeat_play()
            BossCreate = True


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

    for object in LowEnemyList :
        isDel = object.update(frame_time)
        if object.getMissileTime() > 1:
            enemy_missile = EnummyMissile(*object.get_pos())
            ENEMY_MISSILE_LIST.append(enemy_missile)
            object.setMissileTime(0)
        if isDel == True:
            LowEnemyList.remove(object)

    for object in MiddleEnemyList :
        isDel = object.update(frame_time)
        if object.getMissileTime() > 0.5:
            enemy_missile = EnummyMissile(*object.get_pos())
            ENEMY_MISSILE_LIST.append(enemy_missile)
            object.setMissileTime(0)
        if isDel == True:
            MiddleEnemyList.remove(object)

    for object in HighEnemyList :
        isDel = object.update(frame_time)
        if object.Time  > 2:
            enemy_missile1 = MagicMissile(*object.get_left_pos())
            enemy_missile2 = MagicMissile(*object.get_right_pos())
            ENEMY_MISSILE_LIST.append(enemy_missile1)
            ENEMY_MISSILE_LIST.append(enemy_missile2)
            object.setMissileTime(0)
        if isDel == True:
            HighEnemyList.remove(object)

    if BossCreate and boss.HP > 0:
        if boss.specialAttack and boss.Time > 1.5:
            for rad in range(0, 36):
                bossmissile = RotateMissile(boss.x, boss.y, rad)
                ENEMY_MISSILE_LIST.append(bossmissile)
                boss.Time = 0
        elif (not boss.specialAttack) and boss.Time > 0.5:
            boss_missile1 = MagicMissile(*boss.get_left_pos())
            boss_missile2 = MagicMissile(*boss.get_right_pos())
            ENEMY_MISSILE_LIST.append(boss_missile1)
            ENEMY_MISSILE_LIST.append(boss_missile2)
            boss.Time = 0


    for object in ENEMY_MISSILE_LIST :
        isDel = object.update(frame_time)
        if isDel == True :
            ENEMY_MISSILE_LIST.remove(object)

    #필살기
    for object in BombAirplanList :
        isDel = object.update(frame_time)
        if isDel == True :
            BombAirplanList.remove(object)

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

    for enemise in LowEnemyList :
        enemise.draw()
        enemise.draw_box()

    for enemise in MiddleEnemyList :
        enemise.draw()
        enemise.draw_box()

    for enemise in HighEnemyList :
        enemise.draw()
        enemise.draw_box()

    for e_bullet in ENEMY_MISSILE_LIST :
        e_bullet.draw()
        e_bullet.draw_box()

    for explosions in ExplosionList :
        explosions.draw()

    for explosions in BigExplosionList :
        explosions.draw()

    for powerItem in PowerItemList :
        powerItem.draw()

    for bombItem in BombItemList :
        bombItem.draw()

    for bomb in BombAirplanList :
        bomb.draw()
        bomb.draw_box()

    if BossCreate :
        boss.draw()
        boss.draw_box()
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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            if player.boomCount > 0 :
                bombAirplan = BombAirplan()
                BombAirplanList.append(bombAirplan)
                player.set_bombItem(-1)
        else:
            player.handle_event(event)


def pause():
    pass


def resume():
    pass
