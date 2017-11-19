import random

from pico2d import *
import Game_FrameWork


class Player:
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
        self.xMove, self. yMove= 0, 0
        if Player.image == None :
            Player.image = load_image('image\player\player.png')

    def handle_event(self, event):
        #위
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.STAND, self.LEFT, self.RIGHT):
                self.state = self.FORWARD
                self.yMove = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state in (self.FORWARD,):
                self.state = self.STAND
                self.yMove = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.STAND, self.LEFT, self.RIGHT):
                self.state = self.FORWARD
                self.yMove = -1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.FORWARD,):
                self.state = self.STAND
                self.yMove = 0
        pass

    def update(self, frame_time):
        def clamp(minPos, x, maxPos):
            return max(minPos, min(x, maxPos))

        self.frame = (self.frame + 1) % 3
        self.x += self.xMove
        self.y += self.yMove

        self.x = clamp(0, self.x, Game_FrameWork.Width)
        self.y = clamp(0, self.y, Game_FrameWork.Height)
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64,self.x, self.y)