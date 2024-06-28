import time
from tkinter import Canvas

from configuration import FIELD_SIZE, UNIT_SIZE, FRAME_MS
from drawing import Draw
from game_logic import GameLoop
from input_controller import InputController

t = time.time()


class MainField:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(bg="white",
                             height=(FIELD_SIZE[0] + 3.5) * UNIT_SIZE,
                             width=(FIELD_SIZE[1] + 9) * UNIT_SIZE)
        self.canvas.pack()
        control = InputController()
        draw = Draw(self.canvas)
        game_loop = GameLoop()
        control.command(self.canvas)
        self.root.after(FRAME_MS, self.update_game, game_loop, control, draw)

    def update_game(self, game_loop, control, draw):
        # todo почему время больше
        # todo проскакивание слоев
        # рандомное заполнение до определенной высотя
        global t
        current_start_time = time.time()
        previous_start_time = t
        t = current_start_time
        time_between_iterations = current_start_time - previous_start_time

        if not game_loop.you_loose:
            self.root.after(FRAME_MS, self.update_game, game_loop, control, draw)
            control.action_processing(game_loop)
            if game_loop.switch_frame():
                game_loop.speed_up()
                game_loop.create_new_figure()
                game_loop.update_active_figure(game_loop)
                if game_loop.find_filled_rows():
                    game_loop.remove_filled_rows()
                if not game_loop.active_figure:
                    game_loop.activate_figure()
                game_loop.check_loss()
            draw.update_canvas(game_loop)
