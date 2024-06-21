from copy import deepcopy
import random
from typing import List, Optional

from auxillary_functions import initialize_game, remove_cells, switch_state_counterclockwise, switch_state
from configuration import CELL_VALUE, FALL_COORD, FIELD_SIZE, STEP_LEFT_COORD, STEP_RIGHT_COORD, init_time_per_update, \
    relative_coords_library
from figures import Angle, Figure, Origami, Paw, Rectangle, ReverseAngle, ReverseOrigami, Tetris


class GameLoop:
    def __init__(self, time_per_update):
        self.init_field: List[List[int]] = initialize_game()
        self.field: Optional[List[List[int]]] = []
        self.active_figure: Optional[Figure] = None
        self.all_figures: Optional[List[Figure]] = []
        self.you_loose: bool = False
        self.frame_counter = 0
        self.action_sequence = []
        self.filled_row_counter = 0
        self.time_per_update = time_per_update

    def speed_up(self):
        if self.time_per_update > 4:
            self.time_per_update = init_time_per_update - 2 * self.filled_row_counter
            if self.time_per_update < 2:
                print('here error gl-26')

    def switch_frame(self) -> bool:
        self.frame_counter += 1
        update_frame = self.frame_counter == self.time_per_update
        if update_frame:
            self.frame_counter = 0
        return update_frame

    def update_field(self) -> None:
        self.field = deepcopy(self.init_field)
        if self.all_figures:
            for figure in self.all_figures:
                self.place_figure(figure)

    def place_figure(self, figure) -> None:
        for row, column in figure.coord:
            self.field[row][column] = CELL_VALUE[(figure.__repr__())]

    def create_new_figure(self) -> None:
        self.active_figure = random.choice((Origami(), ReverseOrigami(), Rectangle(), Tetris(), Angle(), Paw(), ReverseAngle()))
        self.all_figures.append(self.active_figure)

    def remove_filled_rows(self, row_to_remove) -> None:
        # remove filled row
        coord_to_remove = [[row_num, cell_num] for cell_num in range(FIELD_SIZE[1]) for row_num in row_to_remove]
        for figure in self.all_figures:
            remove_cells(figure, coord_to_remove)
        # filter empty figures
        self.all_figures = [figure for figure in self.all_figures if figure.coord]
        self.shift_upper_rows(row_to_remove)

    def shift_upper_rows(self, row_to_remove):
        for figure in self.all_figures:
            for pair_num in range(len(figure.coord)):
                if figure.coord[pair_num][0] < row_to_remove[0]:
                    figure.coord[pair_num][0] += len(row_to_remove)

    def find_filled_row(self) -> List[int]:
        rows_to_remove = []
        for row_num in range(FIELD_SIZE[0]):
            if all([int(self.field[row_num][cell_num]) == CELL_VALUE['Any_Fig'] for cell_num in range(FIELD_SIZE[1])]):
                rows_to_remove.append(row_num)
        for row in rows_to_remove:
            self.filled_row_counter += 1
        return rows_to_remove

    def check_loss(self):
        for figure in self.all_figures[:-1]:
            for row, column in figure.coord:
                if row in (0, 1, 2):
                    self.you_loose = True
                    return
        # self.update_field()
        # for row, column in self.active_figure.find_coord():
        #     if int(self.field[row][column]) == CELL_VALUE['Any_Fig']:
        #         self.you_loose = True
        #         self.active_figure = None
        #         return


    def update_active_figure(self):
        for row, column in self.active_figure.find_stuck_coord():
            if row < FIELD_SIZE[0] - 1:  # active figure falls on another figure
                if self.field[row + FALL_COORD[0]][column] != CELL_VALUE["Empty"]:
                    self.active_figure = None
                    return
            elif row == FIELD_SIZE[0] - 1:  # active figure falls on flour
                self.active_figure = None
                return
        self.active_figure.fall()

    # SHIFT FIGURE
    def turn_clockwise(self, canvas) -> None:
        self.action_sequence.append('turn_clockwise')

    def turn_counterclockwise(self, canvas) -> None:
        self.action_sequence.append('turn_counterclockwise')

    def step_left(self, canvas) -> None:
        self.action_sequence.append('left')

    def step_right(self, canvas) -> None:
        self.action_sequence.append('right')

    def step_down(self, canvas) -> None:
        self.action_sequence.append('down')

    def action_processing(self) -> None:
        step_directions = {'left': (self.restrict_left_border, STEP_LEFT_COORD, 1),
                           'right': (self.restrict_right_border, STEP_RIGHT_COORD, 1),
                           'down': (self.restrict_height, FALL_COORD, 0)
                           }
        if self.active_figure:
            for action in self.action_sequence:
                if action in ('turn_clockwise', 'turn_counterclockwise'):
                    if self.active_figure.freedom_degree > 1:
                        self.turn_figure(action)
                elif self.is_empty_space(step_directions[action][1]) and step_directions[action][0]():
                    index = step_directions[action][2]
                    self.active_figure.anchor_coord[index] += step_directions[action][1][index]
                    self.active_figure.coord = self.active_figure.find_coord()
            self.action_sequence = []

    def restrict_left_border(self) -> bool:
        return all([column > 0 for row, column in self.active_figure.find_coord()])

    def restrict_right_border(self) -> bool:
        return all([column < FIELD_SIZE[1] - 1 for row, column in self.active_figure.find_coord()])

    def restrict_height(self) -> bool:
        return all([row < FIELD_SIZE[0] - 1 for row, column in self.active_figure.find_coord()])

    def is_empty_space(self, coord_shift: List[int]) -> bool:
        coord_to_try = [[row + coord_shift[0], column + coord_shift[1]] for row, column in self.active_figure.find_coord()]
        for row, column in coord_to_try:
            for figure in self.all_figures[:-1]:
                if [row, column] in figure.coord:
                    return False
        return True

    def turn_figure(self, action: str) -> None:
        # print('bef turn', self.active_figure.coord, self.active_figure.relative_coordinates, 'ind', self.active_figure.state_index, self.active_figure.anchor_coord)
        if action == 'turn_clockwise':
            new_index = switch_state(self.active_figure)
        elif action == 'turn_counterclockwise':
            new_index = switch_state_counterclockwise(self.active_figure)
        print('n ind', new_index)
        coord_to_try = [[row + self.active_figure.anchor_coord[0], column + self.active_figure.anchor_coord[1]]
                        for row, column in relative_coords_library[self.active_figure.__repr__()][new_index]]
        print(self.is_empty_space_to_turn(coord_to_try))
        if self.is_empty_space_to_turn(coord_to_try):
            self.active_figure.coord = coord_to_try
            self.active_figure.relative_coordinates = relative_coords_library[self.active_figure.__repr__()][new_index]
            self.active_figure.state_index = new_index
            self.active_figure.stuck_coord = self.active_figure.find_stuck_coord()
        # print('aft turn', self.active_figure.coord, self.active_figure.relative_coordinates, 'ind', self.active_figure.state_index, '|', self.active_figure.anchor_coord)
        # print()

    def is_empty_space_to_turn(self, coord_to_try) -> bool:
        # todo поиск по неактивным
        # for figure in self.all_figures[-1]:
        #     print(figure.coord)
        #     for row, column in coord_to_try:
        #         print('r c', row, column)
        #         if self.field[row][column] in figure.coord:
        #             print('gere123')
        #             return False
        for row, column in coord_to_try:
            if not (0 <= row < FIELD_SIZE[0] - 1) or not (0 <= column <= FIELD_SIZE[1] - 1):
                return False
        return True
