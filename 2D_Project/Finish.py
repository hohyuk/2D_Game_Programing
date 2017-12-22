import Game_FrameWork
import first_stage_state
import logo_state
from pico2d import *

name = "FinishState"
image = None
ScoreFont = None
font = None
pause_time = 0.0


def enter():
    global image, ScoreFont, font, Count
    image = load_image('image/finish/Clear.png')
    ScoreFont = load_font('font/font01.TTF', 50)
    font = load_font('font/font01.TTF', 30)


def exit():
    global image, font
    del image, font


def update(frame_time):
    pass

def draw(frame_time):
    global image
    clear_canvas()
    first_stage_state.draw_stage_scene()
    image.clip_draw_to_origin(0, 0, 1000, 300, 0, 300, 800, 300)

    font.draw(250,150,"1. 이어하기     2. 종료",(255,0,255))
    ScoreFont.draw(200, 250, " SCORE : %d" % (first_stage_state.score.score), (0, 0, 255))
    ScoreFont.draw(200, 300, " TIME : %02d" % (first_stage_state.score.Time), (255, 255, 0))
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            first_stage_state.player.revive()
            Game_FrameWork.pop_state()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            Game_FrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            Game_FrameWork.pop_state()


def pause():
    pass


def resume():
    pass
