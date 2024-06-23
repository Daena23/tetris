import random
from copy import deepcopy
from typing import List, Optional

from auxillary_functions import is_figure_within_field, remove_cells, switch_state_back, \
    switch_state_forward
from configuration import FALL_COORD, FIELD_SIZE, init_time_per_update
from figures import Angle, Figure, Origami, Paw, Rectangle, ReverseAngle, ReverseOrigami, Tetris


class GameLoop:
    def __init__(self, time_per_update):
        self.next_figure: Optional[Figure] = None
        self.active_figure: Optional[Figure] = None
        self.all_figures: Optional[List[Figure]] = []
        self.you_loose: bool = False
        self.frame_counter: int = 0
        self.time_per_update: int = time_per_update
        self.action: str = ''
        self.filled_row_counter: int = 0

    def speed_up(self):  # todo refactor
        if self.time_per_update > 4:
            self.time_per_update = init_time_per_update - self.filled_row_counter
            if self.time_per_update < 2:
                print('here error gl-26')

    def switch_frame(self) -> bool:   # todo refactor
        self.frame_counter += 1
        update_frame = self.frame_counter == self.time_per_update
        if update_frame:
            self.frame_counter = 0
        return update_frame

    @staticmethod
    def create_new_figure() -> Figure:
        return random.choice((Origami('red'),
                              Paw('violet'),
                              Rectangle('yellow'),
                              Tetris('green'),
                              Angle('blue'),
                              ReverseOrigami('orange'),
                              ReverseAngle('pink')))

    # ROW SHIFT
    def find_filled_row(self) -> List[int]:
        rows_to_remove = []
        lst = []
        for row_num in range(2, FIELD_SIZE[0]):
            # todo НЕ РАБОТАЕТ
            for figure in self.all_figures:
                lst = [(row, column) for row, column in figure.coord if row == row_num]
                if len(set(lst)) == FIELD_SIZE[1] - 1:
                    rows_to_remove.append(row_num)
        # if rows_to_remove:
        #     print('rowstorem', rows_to_remove)
        return rows_to_remove

    def remove_filled_rows(self, row_to_remove) -> None:  # todo убрать - перементсть
        # remove filled row
        coord_to_remove = [[row_num, cell_num] for cell_num in range(FIELD_SIZE[1]) for row_num in row_to_remove]
        for figure in self.all_figures:
            remove_cells(figure, coord_to_remove)
        # filter empty figures
        self.all_figures = [figure for figure in self.all_figures if figure.coord]
        self.shift_upper_rows(row_to_remove)

    def shift_upper_rows(self, row_to_remove: List[List[int]]):
        for figure in self.all_figures:
            for pair_num in range(len(figure.coord)):
                if figure.coord[pair_num][0] < row_to_remove[0]:
                    figure.coord[pair_num][0] += len(row_to_remove)

    def check_loss(self) -> None:
        for figure in self.all_figures[:-1]:
            for row, column in figure.coord:
                if row in (0, 1, 2):
                    self.you_loose = True
                    return

    # def falling_figure_stuck_to_another(self, row: int, column: int) -> bool:
    #     for figure in self.all_figures[:-1]:
    #         if [row + 1, column] in figure.coord:
    #             return True
    #     return False

    def update_active_figure(self):
        coord_to_try = [[row + 1, column] for row, column in self.active_figure.find_coord()]
        if not is_figure_within_field(coord_to_try) or self.is_intersection(coord_to_try):
            self.active_figure = None
            return
        self.active_figure.anchor_coord[0] += FALL_COORD[0]
        self.active_figure.coord = self.active_figure.find_coord()

    # SHIFT FIGURES
    def turn(self, canvas) -> None:
        self.action = 'turn'

    def turn_back(self, canvas) -> None:
        self.action = 'turn_back'

    def step_left(self, canvas) -> None:
        self.action = 'left'

    def step_right(self, canvas) -> None:
        self.action = 'right'

    def step_down(self, canvas) -> None:
        self.action = 'down'

    def action_processing(self) -> None:
        # rotation
        if self.active_figure and self.action:
            if self.action in ('turn', 'turn_back') and self.active_figure.freedom_degree > 1:
                self.turn_figure()
        # shift
            else:
                direct = {'left': (0, -1),
                          'right': (0, 1),
                          'down': (1, 0)
                          }
                shift_row, shift_column = list(direct[self.action])
                try_coord = [[row + shift_row, column + shift_column] for row, column in self.active_figure.find_coord()]
                if is_figure_within_field(try_coord) and not self.is_intersection(try_coord):
                    self.active_figure.anchor_coord[0] += shift_row
                    self.active_figure.anchor_coord[1] += shift_column
                    self.active_figure.coord = self.active_figure.find_coord()
            self.action = ''

    def turn_figure(self) -> None:
        new_index = switch_state_forward(self.active_figure) if self.action == 'turn' else switch_state_back(self.active_figure)
        try_rel_coord = self.active_figure.relative_coord_library[new_index]
        try_coord = [[row + self.active_figure.anchor_coord[0], column + self.active_figure.anchor_coord[1]]
                     for row, column in try_rel_coord]
        if is_figure_within_field(try_coord) and not self.is_intersection(try_coord):
            self.active_figure.state_index = new_index
            self.active_figure.relative_coord = self.active_figure.relative_coord_library[new_index]
            self.active_figure.coord = try_coord.copy()

    def is_intersection(self, try_coord: List[List[int]]):
        for row, column in try_coord:
            for figure in self.all_figures[:-1]:
                if [row, column] in figure.coord:
                    return True
        return False
