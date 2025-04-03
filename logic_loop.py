import random
from copy import copy
from typing import List, Optional

from utils import define_random_coord, is_figure_within_field, is_intersection
from configuration import SWITCHING_FRAME_COEFFICIENT, FALL_COORD, FIELD_SIZE, HOW_OFTEN_SPEED_UP, LEVELS_FOR_WIN, MAX_SPEED, SPEED_GROWTH
from figures import Angle, Figure, NoodlesFigure, Origami, Paw, Rectangle, ReverseAngle, ReverseOrigami, Tetris


class LogicLoop:
    def __init__(self):
        self.next_figure: Optional[Figure] = None
        self.active_figure: Optional[Figure] = None
        self.all_figures: Optional[List[Figure]] = []
        self.you_loose: bool = False
        self.you_won: bool = False
        self.frame_counter: int = 0
        self.action: str = ''
        self.rows_to_remove = []
        self.speed: int = 10
        self.score: int = 0
        self.total_filled_rows: int = 0
        self.increase_speed = False
        self.time_remained_to_spawn_figure: int = 0

    # CYCLE CHECKPOINTS
    def speed_up(self) -> None:
        if self.total_filled_rows % HOW_OFTEN_SPEED_UP == 0 and self.increase_speed:
            self.increase_speed = False
            if self.speed < MAX_SPEED:
                self.speed += SPEED_GROWTH

    def switch_frame(self) -> bool:
        self.frame_counter += 1
        if self.frame_counter == SWITCHING_FRAME_COEFFICIENT // self.speed:
            self.frame_counter = 0
            return True
        return False

    def create_noodle_figure(self) -> None:
        coordinates = define_random_coord()
        for coord in coordinates:
            self.all_figures.append(NoodlesFigure(random.choice(("#f26d49", "#539cd9", "#37a237", "#f9eb76")), coord))

    def check_if_won(self, game_type: str) -> None:
        if game_type == 'A' and self.total_filled_rows >= LEVELS_FOR_WIN:
            self.you_won = True

    # ACTIVE FIGURE
    def create_init_figures(self) -> None:
        self.create_new_figure()
        self.active_figure = copy(self.next_figure)
        self.all_figures.append(self.active_figure)
        self.create_new_figure()

    def create_new_figure(self) -> None:
        self.next_figure = random.choice((Tetris('#37a237'),
                                          Origami('#f26d49'),
                                          Paw('violet'),
                                          Rectangle('#f9eb76'),
                                          Angle('#539cd9'),
                                          ReverseOrigami('orange'),
                                          ReverseAngle('pink')))

    def activate_figure(self) -> None:
        self.active_figure = copy(self.next_figure)
        self.all_figures.append(self.active_figure)
        self.create_new_figure()
        if is_intersection(self, self.active_figure.coord):
            self.you_loose = True
            self.score = self.total_filled_rows * 1000
            return

    def update_active_figure(self) -> None:
        coord_to_try: List[List[int]] = \
            [[row + FALL_COORD[0], column] for row, column in self.active_figure.find_coord()]
        if not is_figure_within_field(coord_to_try) or is_intersection(self, coord_to_try):
            self.active_figure: Optional[Figure] = None
            return
        self.active_figure.anchor_coord[0] += FALL_COORD[0]
        self.active_figure.coord = self.active_figure.find_coord()

# REMOVE ROWS
    def find_filled_rows(self) -> List[int]:
        if self.all_figures:
            self.rows_to_remove = []
            for row_num in range(1, FIELD_SIZE[0]):
                row_coord = []
                for figure in self.all_figures:
                    row_coord.extend([(row, column) for row, column in figure.coord if row == row_num])
                if len(set(row_coord)) == FIELD_SIZE[1]:
                    self.rows_to_remove.append(row_num)
                    self.increase_speed = True
            if len(self.rows_to_remove) > 0:
                self.total_filled_rows += len(self.rows_to_remove)
                self.active_figure = None
            return self.rows_to_remove

    def remove_filled_rows(self) -> None:
        # filter filled row
        coord_to_remove = [[row, column] for column in range(FIELD_SIZE[1]) for row in self.rows_to_remove]
        for figure in self.all_figures:
            for coord in coord_to_remove:
                if coord in figure.coord:
                    figure.coord.remove(coord)
        # filter empty figures
        self.all_figures = [figure for figure in self.all_figures if figure.coord]
        self.shift_upper_rows(self.rows_to_remove)

    def shift_upper_rows(self, row_to_remove: List[List[int]]) -> None:
        for figure in self.all_figures:
            for pair_num in range(len(figure.coord)):
                for row_num in row_to_remove:
                    if figure.coord[pair_num][0] < row_num:
                        figure.coord[pair_num][0] += 1
