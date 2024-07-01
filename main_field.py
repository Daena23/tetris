from tkinter import Canvas

from configuration import FIELD_SIZE, FRAME_MS, UNIT_SIZE
from drawing import GameField
from logic_loop import LogicLoop
from input_controller import InputController


class MainLoop:
    def __init__(self, root, game_type):
        self.root = root
        self.game_type = game_type
        self.canvas = Canvas(bg="white",
                             height=(FIELD_SIZE[0] + 3.5) * UNIT_SIZE,
                             width=(FIELD_SIZE[1] + 9) * UNIT_SIZE)
        self.canvas.pack()
        draw = GameField(self.canvas)
        control = InputController()
        log_loop = LogicLoop()
        if self.game_type == 'B':
            log_loop.create_noodle_figure()
        log_loop.create_init_figures()
        control.command(draw.canvas)
        self.root.after(FRAME_MS, self.update_game, log_loop, control, draw, self.game_type)

    def update_game(self, game_loop, control, draw, game_type):
        if not (game_loop.you_loose or game_loop.you_won):
            self.root.after(FRAME_MS, self.update_game, game_loop, control, draw, game_type)
            control.action_processing(game_loop)
            if game_loop.switch_frame():
                if self.game_type == 'A':
                    game_loop.speed_up()
                if game_loop.time_remained_to_spawn != 0:
                    game_loop.time_remained_to_spawn -= 1
                if game_loop.active_figure is None:
                    if game_loop.find_filled_rows():
                        game_loop.remove_filled_rows()
                        game_loop.check_win(game_type)
                        game_loop.time_remained_to_spawn = 2  # choose the constant of your choice
                    if game_loop.time_remained_to_spawn == 0:
                        game_loop.activate_figure()
                else:
                    game_loop.update_active_figure()
            draw.update_canvas(game_loop)
