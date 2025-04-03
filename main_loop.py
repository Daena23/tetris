from tkinter import Canvas

from configuration import FIELD_SIZE, FRAME_MS, UNIT_SIZE
from draw_canvas import DrawCanvas
from logic_loop import LogicLoop
from input_controller import InputController


class MainLoop:
    def __init__(self, root, game_type: str):
        self.root = root
        self.game_type = game_type
        self.canvas = Canvas(
            bg="white",
            height=(FIELD_SIZE[0] + 3.5) * UNIT_SIZE,
            width=(FIELD_SIZE[1] + 9) * UNIT_SIZE,
        )
        self.canvas.pack()
        drawing = DrawCanvas(self.canvas)
        control = InputController()
        logic_loop = LogicLoop()
        if self.game_type == 'B':
            logic_loop.create_noodle_figure()
        logic_loop.create_init_figures()
        control.command(drawing.canvas)
        self.root.after(FRAME_MS, self.update_game, logic_loop, control, drawing)

    def update_game(self, logic_loop: LogicLoop, control: InputController, drawing: DrawCanvas) -> None:
        if not (logic_loop.you_loose or logic_loop.you_won):
            self.root.after(FRAME_MS, self.update_game, logic_loop, control, drawing)
            control.action_processing(logic_loop)
            if logic_loop.switch_frame():
                if self.game_type == 'A':
                    logic_loop.speed_up()
                if logic_loop.time_remained_to_spawn_figure != 0:
                    logic_loop.time_remained_to_spawn_figure -= 1
                if logic_loop.active_figure is None:
                    if logic_loop.find_filled_rows():
                        logic_loop.remove_filled_rows()
                        logic_loop.check_if_won(self.game_type)
                        logic_loop.time_remained_to_spawn_figure = 2  # choose the constant of your choice
                    if logic_loop.time_remained_to_spawn_figure == 0:
                        logic_loop.activate_figure()
                else:
                    logic_loop.update_active_figure()
            drawing.update_canvas(logic_loop)
