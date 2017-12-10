from pico2d import *

import Game_FrameWork

class Score:
    font = None
    def __init__(self):
        self.font = load_font('font/font01.TTF', 30)
        self.score = 0
        self.Time = 0.0
    def setScore(self,addScore):
        self.score += addScore
    def setTime(self,addTime):
        self.Time = (addTime%600)
    def draw(self):
        self.font.draw(600,570," SCORE : %d"%(self.score), (0,0,255))
        self.font.draw(400, 570, " TIME : %02d" % (self.Time), (255, 255, 0))