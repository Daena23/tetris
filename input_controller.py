from typing import Set

from typing_extensions import Optional

from utils import is_figure_within_field, is_intersection, switch_back, switch_forward


class InputController:
    def __init__(self):
        self.action: Optional[str] = None
        self.pressed_key: Set = set()

    def command(self, canvas):
        canvas.bind_all("<KeyPress-Left>", self.step_left)
        canvas.bind_all("<KeyPress-Right>", self.step_right)
        canvas.bind_all("<KeyPress-Down>", self.step_down)
        for z in 'Zz':
            canvas.bind_all(f"<KeyPress-{z}>", self.turn)
            canvas.bind_all(f"<KeyRelease-{z}>", self.turn_release)
        for x in 'Xx':
            canvas.bind_all(f"<KeyPress-{x}>", self.turn_back)
            canvas.bind_all(f"<KeyRelease-{x}>", self.turn_back_release)

    def turn(self, event) -> None:
        if event.keysym not in self.pressed_key:
            self.action = 'turn'
            self.pressed_key.add(event.keysym)

    def turn_release(self, event):
        if event.keysym in self.pressed_key:
            self.pressed_key.remove(event.keysym)

    def turn_back(self, event) -> None:
        if event.keysym not in self.pressed_key:
            self.action = 'turn_back'
            self.pressed_key.add(event.keysym)

    def turn_back_release(self, event):
        if event.keysym in self.pressed_key:
            self.pressed_key.remove(event.keysym)

    def step_left(self, event) -> None:
        self.action: str = 'left'

    def step_right(self, event) -> None:
        self.action: str = 'right'

    def step_down(self, event) -> None:
        self.action: str = 'down'

    def action_processing(self, logic_loop) -> None:
        # to rotate
        if logic_loop.active_figure and self.action:
            if self.action in ('turn', 'turn_back'):
                self.turn_figure(logic_loop)
        # to shift
            else:
                direction = {
                    'left': (0, -1),
                    'right': (0, 1),
                    'down': (1, 0),
                }
                shift_row, shift_column = list(direction[self.action])
                coord_to_try = []
                for row, column in logic_loop.active_figure.find_coord():
                    coord_to_try.append([row + shift_row, column + shift_column])
                if is_figure_within_field(coord_to_try) and not is_intersection(logic_loop, coord_to_try):
                    logic_loop.active_figure.anchor_coord[0] += shift_row
                    logic_loop.active_figure.anchor_coord[1] += shift_column
                    logic_loop.active_figure.coord = logic_loop.active_figure.find_coord()
            self.action = ''

    def turn_figure(self, logic_loop) -> None:
        if logic_loop.active_figure.freedom_degree > 1:
            if self.action == 'turn':
                new_index = switch_forward(logic_loop.active_figure)
            else:
                new_index = switch_back(logic_loop.active_figure)
            try_rel_coord = logic_loop.active_figure.relative_coord_library[new_index]
            coord_to_try = []
            for row, column in try_rel_coord:
                coord_to_try.append(
                    [row + logic_loop.active_figure.anchor_coord[0], column + logic_loop.active_figure.anchor_coord[1]])
            if is_figure_within_field(coord_to_try) and not is_intersection(logic_loop, coord_to_try):
                logic_loop.active_figure.state_index = new_index
                logic_loop.active_figure.relative_coord = logic_loop.active_figure.relative_coord_library[new_index]
                logic_loop.active_figure.coord = coord_to_try.copy()
