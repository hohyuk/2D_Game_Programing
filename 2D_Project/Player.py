import random

from pico2d import *

import Game_FrameWork


class Player:
    PLAYER_SIZE = 64

    PIXEL_PER_METER = (10.0 / 0.7)          # 10 pixel 70cm
    FLY_SPEED_KMPH = 50.0
    FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
    FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
    FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

    STAND, FORWARD, RIGHT, LEFT = 0, 1, 2, 3

    image = None

    def __init__(self):
        self.frame = 0
        self.state = self.STAND
        self.x, self.y = 400, 90
        self.xDir, self. yDir = 0, 0

        Player.image = load_image('image/player/player.png')


    def get_pos(self):
        print(self.x,self.y)
        return self.x, self.y

    def handle_event(self, event):
        # 위
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.STAND, self.LEFT, self.RIGHT):
                self.state = self.FORWARD
                self.yDir = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state in (self.FORWARD, self.LEFT, self.RIGHT):
                self.state = self.STAND
                self.xDir = 0
                self.yDir = 0
        # 아래
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.STAND, self.LEFT, self.RIGHT):
                self.state = self.STAND
                self.yDir = -1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.STAND,):
                self.state = self.STAND
                self.xDir = 0
                self.yDir = 0
        # 왼쪽
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.STAND, self.FORWARD, self.RIGHT):
                self.state = self.LEFT
                self.xDir = -1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT, self.FORWARD):
                self.state = self.STAND
                self.xDir = 0
                self.yDir = 0
        # 오른쪽
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.STAND, self.FORWARD, self.LEFT):
                self.state = self.RIGHT
                self.xDir = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT,):
                self.state = self.STAND
                self.xDir = 0
                self.yDir = 0
        pass

    def update(self, frame_time):
        def clamp(minPos, x, maxPos):
            return max(minPos, min(x, maxPos))

        self.frame = (self.frame + 1) % 3
        self.x += self.xDir
        self.y += self.yDir

        self.x = clamp((Player.PLAYER_SIZE / 2), self.x, Game_FrameWork.Width-(Player.PLAYER_SIZE / 2))
        self.y = clamp((Player.PLAYER_SIZE / 2), self.y, Game_FrameWork.Height-(Player.PLAYER_SIZE / 2))
        pass

    def draw(self):
        self.image.clip_draw(self.frame * Player.PLAYER_SIZE, self.state * Player.PLAYER_SIZE
                             , Player.PLAYER_SIZE, Player.PLAYER_SIZE,self.x, self.y)