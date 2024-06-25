from copy import copy
from tkinter import Canvas

from configuration import FIELD_SIZE, UNIT_SIZE, frame_ms, init_time_per_update
from drawing import Draw
from game_logic import GameLoop


class MainField:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(bg="white",
                             height=(FIELD_SIZE[0] + 2) * UNIT_SIZE,
                             width=(FIELD_SIZE[1] + 9) * UNIT_SIZE)
        self.canvas.pack()
        draw = Draw(self.canvas)
        game_loop = GameLoop(init_time_per_update)
        self.command(game_loop)
        self.root.after(frame_ms, self.update_game, draw, game_loop)

    def command(self, game_loop):
        self.canvas.bind_all("<KeyPress-Left>", game_loop.step_left)
        self.canvas.bind_all("<KeyPress-Right>", game_loop.step_right)
        self.canvas.bind_all("<KeyPress-Down>", game_loop.step_down)
        for x in ('X', 'x'):
            self.canvas.bind_all(f"<KeyPress-{x}>", game_loop.turn)
        for z in ('Z', 'z'):
            self.canvas.bind_all(f"<KeyPress-{z}>", game_loop.turn_back)

    def update_game(self, draw, game_loop):
        # todo ошибка при конце игры loose - более или менее подправила
        # todo key release
        # todo надо отладить SCORE
        # KeyError: 'turn_back'

        if not game_loop.you_loose:
            self.root.after(frame_ms, self.update_game, draw, game_loop)
            game_loop.action_processing()
            if game_loop.switch_frame():  # todo score
                # game_loop.speed_up()
                # act fig входит в allfig
                game_loop.create_new_figure()
                game_loop.update_active_figure()
                if game_loop.find_filled_rows():
                    game_loop.remove_filled_rows()
                if not game_loop.active_figure:
                    game_loop.activate_figure()
                game_loop.check_loss()
            draw.update_canvas(game_loop)
