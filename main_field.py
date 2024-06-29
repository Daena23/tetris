from tkinter import Canvas

from configuration import FIELD_SIZE, UNIT_SIZE, FRAME_MS
from drawing import Draw
from game_logic import GameLoop
from input_controller import InputController


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
        game_loop.create_noodle_figure()
        game_loop.create_init_figures()
        control.command(self.canvas)
        self.root.after(FRAME_MS, self.update_game, game_loop, control, draw)

    def update_game(self, game_loop, control, draw):
        # баг при снимании соля дырчатость
        if not game_loop.you_loose:
            self.root.after(FRAME_MS, self.update_game, game_loop, control, draw)
            control.action_processing(game_loop)
            if game_loop.switch_frame():
                # game_loop.speed_up()
                if game_loop.time_remained_to_spawn != 0:
                    game_loop.time_remained_to_spawn -= 1
                if game_loop.active_figure is None and game_loop.all_figures:
                    if game_loop.find_filled_rows():
                        game_loop.remove_filled_rows()
                        game_loop.time_remained_to_spawn = 2  # choose the constant of your choice
                if game_loop.active_figure is None and game_loop.time_remained_to_spawn == 0:
                    game_loop.activate_figure()
                if game_loop.active_figure is not None:
                    game_loop.update_active_figure()
            draw.update_canvas(game_loop)
