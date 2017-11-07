import Game_FrameWork
import first_stage_state

from pico2d import *

name = "PauseState"
image = None
pause_time = 0.0
pause_count = 0


def enter():
    global image
    image = load_image('image\pause\pause.png')


def exit():
    global image
    del image


def update():
    global pause_count
    pause_count = (pause_count + 1) % 500


def draw():
    global image
    clear_canvas()
    first_stage_state.draw_stage_scene()
    if pause_count < 300 :
        image.draw(400,300)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            Game_FrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            Game_FrameWork.pop_state()


def pause():
    pass


def resume():
    pass

