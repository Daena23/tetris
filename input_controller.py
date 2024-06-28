from auxillary_functions import is_figure_within_field, is_intersection, switch_back, switch_forward


class InputController:
    def __init__(self):
        self.action = None
        self.pressed_key = set()

    def command(self, canvas):
        canvas.bind_all("<KeyPress-Left>", self.step_left)
        canvas.bind_all("<KeyPress-Right>", self.step_right)
        canvas.bind_all("<KeyPress-Down>", self.step_down)
        for z in ('Z', 'z'):
            canvas.bind_all(f"<KeyPress-{z}>", self.turn)
            canvas.bind_all(f"<KeyRelease-{z}>", self.turn_release)
        for x in ('X', 'x'):
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

    def step_left(self, canvas) -> None:
        self.action = 'left'

    def step_right(self, canvas) -> None:
        self.action = 'right'

    def step_down(self, canvas) -> None:
        self.action = 'down'

    def action_processing(self, game_loop) -> None:
        # rotation
        if game_loop.active_figure and self.action:
            if self.action in ('turn', 'turn_back'):
                self.turn_figure(game_loop)
        # shift
            else:
                direct = {'left': (0, -1),
                          'right': (0, 1),
                          'down': (1, 0)
                          }
                shift_row, shift_column = list(direct[self.action])
                coord_to_try = [[row + shift_row, column + shift_column] for row, column in game_loop.active_figure.find_coord()]
                if is_figure_within_field(coord_to_try) and not is_intersection(game_loop, coord_to_try):
                    game_loop.active_figure.anchor_coord[0] += shift_row
                    game_loop.active_figure.anchor_coord[1] += shift_column
                    game_loop.active_figure.coord = game_loop.active_figure.find_coord()
            self.action = ''

    def turn_figure(self, game_loop) -> None:
        if game_loop.active_figure.freedom_degree > 1:
            if self.action == 'turn':
                new_index = switch_forward(game_loop.active_figure)
            else:
                new_index = switch_back(game_loop.active_figure)
            try_rel_coord = game_loop.active_figure.rel_coord_library[new_index]
            coord_to_try = []
            for row, column in try_rel_coord:
                coord_to_try.append([row + game_loop.active_figure.anchor_coord[0], column + game_loop.active_figure.anchor_coord[1]])
            if is_figure_within_field(coord_to_try) and not is_intersection(game_loop, coord_to_try):
                game_loop.active_figure.state_index = new_index
                game_loop.active_figure.rel_coord = game_loop.active_figure.rel_coord_library[new_index]
                game_loop.active_figure.coord = coord_to_try.copy()
