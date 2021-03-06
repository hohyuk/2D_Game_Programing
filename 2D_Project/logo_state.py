from pico2d import *
import Game_FrameWork
import first_stage_state

name = "LogoState"

logo = None
button = None


class Logo:
    def __init__(self):
        self.image = load_image('image\logo\logo.png')
        # Sound
        self.bgm = load_music('sound/ophelia.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def draw(self):
        self.image.draw(400, 300)


class Button:
    def __init__(self):
        self.image = load_image('image\logo\start_key.png')
        self.flash_count = 0        # 버튼 깜박임.

    def update(self):
        self.flash_count = (self.flash_count + 1) % 500

    def draw(self):
        self.image.draw(400, 100)


def enter():
    global logo, button
    logo = Logo()
    button = Button()


def exit():
    global logo, button
    del logo
    del button


def update(frame_time):
    button.update()


def draw(frame_time):
    clear_canvas()
    logo.draw()
    if button.flash_count < 300:
        button.draw()
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Game_FrameWork.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):         # enter key
                Game_FrameWork.change_state(first_stage_state)


def pause():
    pass


def resume():
    pass

