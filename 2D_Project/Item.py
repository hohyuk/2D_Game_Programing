from pico2d import *
import Game_FrameWork
import random


class Item:
    LEFT_DIR, RIGHT_DIR = 0, 1
    itemSound = None

    def handle_LeftDir(self):
        self.x -= 0.5
        self.dir = self.LEFT_DIR
        if self.x < 0:
            self.dir = self.RIGHT_DIR
            self.x = 0
        if self.dirTime > 5:
            self.dir = self.RIGHT_DIR
            self.dirTime = 0

    def handle_RightDir(self):
        self.x += 0.5
        self.dir = self.RIGHT_DIR
        if self.x > 800:
            self.dir = self.LEFT_DIR
            self.x = 800
        if self.dirTime > 5:
            self.dir = self.LEFT_DIR
            self.dirTime = 0

    handle_dir = {
        LEFT_DIR: handle_LeftDir,
        RIGHT_DIR: handle_RightDir,
    }


class PowerItem(Item):
    SIZE = 50
    image = None
    LEFT_DIR, RIGHT_DIR = 0, 1

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 600
        self.frame = 0
        self.time = 0
        self.dir = random.randint(0, 1)
        self.dirTime = 0
        PowerItem.image = load_image('image/item/Item_Power.png')
        if Item.itemSound == None:
            Item.itemSound = load_wav('sound/Item.wav')
            Item.itemSound.set_volume(64)

    def update(self,frame_time):
        self.time += frame_time * 10
        self.dirTime += frame_time
        if self.time > 1:
            self.frame = (self.frame + 1) % 6
            self.time = 0

        self.handle_dir[self.dir](self)
        self.y -= 0.5
        if self.y < 0:
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * PowerItem.SIZE, 0
                             , PowerItem.SIZE, 35, self.x, self.y)

    def get_size(self):
        return self.x - (PowerItem.SIZE/2), self.y - (35/2), self.x + (PowerItem.SIZE/2), self.y + (35/2)

    def draw_box(self):
        draw_rectangle(*self.get_size ())


class BombItem(Item):
    SIZEX = 54
    SIZEY = 32
    image = None
    LEFT_DIR, RIGHT_DIR = 0, 1

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 600
        self.frame = 0
        self.time = 0
        self.dir = random.randint(0, 1)
        self.dirTime = 0
        BombItem.image = load_image('image/item/Item_Bomb.png')
        if Item.itemSound == None:
            Item.itemSound = load_wav('sound/Item.wav')
            Item.itemSound.set_volume(64)

    def update(self, frame_time):
        self.time += frame_time * 10
        self.dirTime += frame_time
        if self.time > 1:
            self.frame = (self.frame + 1) % 4
            self.time = 0

        self.handle_dir[self.dir](self)
        self.y -= 0.5
        if self.y < 0:
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * BombItem.SIZEX, 0
                             , BombItem.SIZEX, BombItem.SIZEY, self.x, self.y)

    def get_size(self):
        return self.x - (BombItem.SIZEX / 2), self.y - (BombItem.SIZEY / 2), self.x + (BombItem.SIZEX / 2), self.y + \
               (BombItem.SIZEY / 2)

    def draw_box(self):
        draw_rectangle(*self.get_size())