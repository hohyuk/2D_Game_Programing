import Game_FrameWork
import first_stage_state
import logo_state
from pico2d import *

name = "GameOverState"
image = None
CountFont = None
font = None
pause_time = 0.0
Count = 0


def enter():
    global image, CountFont, font, Count
    image = load_image('image\gameover\GameOver.png')
    CountFont = load_font('font/font01.TTF', 300)
    font = load_font('font/font01.TTF', 30)
    Count =10

def exit():
    global image, CountFont, font
    del image, CountFont, font


def update(frame_time):
    global Count
    if Count >= 0 :
        Count -= frame_time


def draw(frame_time):
    global image
    clear_canvas()
    first_stage_state.draw_stage_scene()
    if Count < 0 :
        image.draw(400, 400)
    else :
        CountFont.draw(300,400, "%d"%(Count),(255,100,0))
        font.draw(250,200,"1. 이어하기     2. 종료",(255,0,255))
        font.draw(600, 570, " SCORE : %d" % (first_stage_state.score.score), (0, 0, 255))
        font.draw(400, 570, " TIME : %02d" % (first_stage_state.score.Time), (255, 255, 0))
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            first_stage_state.player.HP = 180
            Game_FrameWork.pop_state()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            Game_FrameWork.pop_state()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
            Game_FrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            Game_FrameWork.pop_state()


def pause():
    pass


def resume():
    pass
