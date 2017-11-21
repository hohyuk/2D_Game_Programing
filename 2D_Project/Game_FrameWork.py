# 파일 앞에 숫자는 못온다. 예) 2D_Game_FrameWork.py
import time

Width = 800
Height = 600


class GameState:
    def __init__(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.pause = state.pause
        self.resume = state.resume
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw


class TestGameState:
    def __init__(self, name):
        self.name= name

    def enter(self):
        print("State [%s] Entered." % self.name)

    def exit(self):
        print("State [%s] Exited." % self.name)

    def pause(self):
        print("State [%s] Paused." % self.name)

    def resume(self):
        print("State [%s] Resumed." % self.name)

    def handle_events(self, frame_time):
        print("State [%s] handle_events." % (self.name, frame_time))

    def update(self, frame_time):
        print("State [%s] update." % (self.name, frame_time))

    def draw(self, frame_time):
        print("State [%s] draw." % (self.name, frame_time))


running = None
stack = None


def change_state(state):
    global stack
    pop_state()
    stack.append(state)
    state.enter()


def push_state(state):
    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(state)
    state.enter()


def pop_state():
    global stack
    if len(stack) > 0:
        stack[-1].exit()
        stack.pop()
    if len(stack) > 0:
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_state):
    global running, stack
    running = True
    stack = [start_state]
    start_state.enter()
    current_time = time.clock()
    while running:
        frame_time = time.clock() - current_time
        current_time += frame_time
        stack[-1].handle_events(frame_time)
        stack[-1].update(frame_time)
        stack[-1].draw(frame_time)

    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()

def reset_time():
    global current_time
    current_time = time.clock()


def test_game_framework():
    start_state = TestGameState('StartState')
    run(start_state)


if __name__ == '__main__' :
    test_game_framework()