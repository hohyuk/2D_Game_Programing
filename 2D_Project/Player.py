import random

from pico2d import *

from HP_UI import *
from Explosion import PlayerExplosion
import Game_FrameWork


class Player:
    PLAYER_SIZE = 64
    PLAYER_EXPLOSION_SIZE =128
    PLAYER_HALF_SIZE_X = 25
    PLAYER_HALF_SIZE_Y = 30
    PIXEL_PER_METER = (10.0 / 22.25)          # 10 pixel 22.25m -> 22.25cm -> 73fit
    FLY_SPEED_KMPH = 2400.0                   # 2마하 -> 약 2400km
    FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
    FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
    FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

    STAND, BACK, FORWARD, LEFT, RIGHT = 0, 1, 2, 3, 4

    image = None
    missileSound = None

    def __init__(self):
        self.frame = 0
        self.state = self.STAND
        self.x, self.y = 400, 90
        self.xDir, self. yDir = 0, 0
        self.HP = 180
        self.HpBar = PlayerHpBar()
        self.HpGauge = PlayerHpGauge()
        self.Explosion = None
        self.isExplosion = False
        Player.image = load_image('image/player/player.png')

        if Player.missileSound == None:
            Player.missileSound = load_wav('sound/Missile.wav')
            Player.missileSound.set_volume(64)

    def update(self, frame_time):
        if self.HP > 0 :
            distance = Player.FLY_SPEED_PPS * frame_time
            if self.state in (self.STAND, self.FORWARD, self.BACK):
                self.frame = (self.frame + 1) % 3
            elif self.state in (self.LEFT, self.RIGHT):
                self.frame = 2

            self.x += (self.xDir * distance)
            self.y += (self.yDir * distance)

            self.x = clamp(self.PLAYER_HALF_SIZE_X, self.x, Game_FrameWork.Width - self.PLAYER_HALF_SIZE_X)
            self.y = clamp(self.PLAYER_HALF_SIZE_Y, self.y, Game_FrameWork.Height - self.PLAYER_HALF_SIZE_Y)
        else:
            if self.Explosion == None:
                self.Explosion = PlayerExplosion(self.x, self.y)
            else:
                self.Explosion.update(frame_time)


    def handle_event(self, event):
        # 위
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.STAND, self.LEFT, self.RIGHT):
                self.state = self.FORWARD
                self.yDir = 1

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state in (self.FORWARD,):
                self.state = self.STAND
                self.frame = 0
                self.xDir = 0
                self.yDir = 0

        # 아래
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.STAND, self.FORWARD, self.LEFT, self.RIGHT):
                self.state = self.BACK
                self.yDir = -1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.BACK,):
                self.state = self.STAND
                self.frame = 0
                self.xDir = 0
                self.yDir = 0
        # 왼쪽
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.FORWARD, self.BACK, self.STAND, self.RIGHT):
                self.state = self.LEFT
                self.xDir = -1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT, ):
                self.state = self.STAND
                self.frame = 0
                self.xDir = 0
                self.yDir = 0

        # 오른쪽
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.FORWARD, self.BACK, self.STAND, self.LEFT):
                self.state = self.RIGHT
                self.xDir = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT,):
                self.state = self.STAND
                self.frame = 0
                self.xDir = 0
                self.yDir = 0

    def draw(self):
        if self.HP > 0:
            self.image.clip_draw(self.frame * Player.PLAYER_SIZE, self.state * Player.PLAYER_SIZE
                             , Player.PLAYER_SIZE, Player.PLAYER_SIZE, self.x, self.y)
        elif self.Explosion != None:
            self.Explosion.draw()
        self.HpBar.draw()
        self.HpGauge.draw(self.HP)

    def get_pos(self):
        self.missileSound.play()
        return self.x, self.y

    def get_HP(self):
        return self.HP

    def set_damage(self,damage):
        self.HP -= damage

    def get_size(self):
        return self.x - self.PLAYER_HALF_SIZE_X, self.y - self.PLAYER_HALF_SIZE_Y, self.x + self.PLAYER_HALF_SIZE_X, \
               self.y + self.PLAYER_HALF_SIZE_Y

    def draw_box(self):
        draw_rectangle(*self.get_size())
