from tkinter import Canvas
from configuration import FIELD_SIZE, frame_ms, init_time_per_update, unit_size
from drawing import Draw
from game_logic import GameLoop


class MainField:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(bg="white",
                             height=(FIELD_SIZE[0] + 2) * unit_size,
                             width=(FIELD_SIZE[1] + 2.5) * unit_size)
        self.canvas.pack()
        draw = Draw(self.canvas)
        game_loop = GameLoop(init_time_per_update)
        self.command(game_loop)
        self.root.after(frame_ms, self.update_game, draw, game_loop)

    def command(self, game_loop):
        self.canvas.bind_all("<KeyPress-Left>", game_loop.step_left)
        self.canvas.bind_all("<KeyPress-Right>", game_loop.step_right)
        self.canvas.bind_all("<KeyPress-Down>", game_loop.step_down)
        self.canvas.bind_all("<KeyPress-z>", game_loop.turn)
        for z in ('Z', 'z'):
            self.canvas.bind_all(f"<KeyPress-{z}>", game_loop.turn)

    def update_game(self, draw, game_loop):
        # todo почему фигкра генерируется в середине поля
        # todo обратное вращение
        # todo слипание при кручении
        # todo ошибка при конце игры loose - более или менее подправила

        if not game_loop.you_loose:
            self.root.after(frame_ms, self.update_game, draw, game_loop)
            game_loop.action_processing()
            if game_loop.switch_frame():
                # game_loop.speed_up()  # todo надо отладить
                game_loop.update_field()
                if game_loop.active_figure:
                    game_loop.update_active_figure()
                else:
                    row_to_remove = game_loop.find_filled_row()
                    if row_to_remove:
                        game_loop.remove_filled_rows(row_to_remove)
                    else:
                        game_loop.create_new_figure()
                        print(game_loop.active_figure.find_coord())
                        print(game_loop.active_figure, game_loop.active_figure.find_coord())
                        game_loop.check_loss()
            draw.update_canvas(game_loop)
