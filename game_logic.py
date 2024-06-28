import random
from copy import copy
from typing import List, Optional

from auxillary_functions import is_figure_within_field, is_intersection
from configuration import COEFFICIENT, FALL_COORD, FIELD_SIZE, FREQUENCY, MAX_SPEED, SPEED_GROWTH
from figures import Angle, Figure, Origami, Paw, Rectangle, ReverseAngle, ReverseOrigami, Tetris


class GameLoop:
    def __init__(self):
        self.next_figure: Optional[Figure] = None
        self.active_figure: Optional[Figure] = None
        self.all_figures: Optional[List[Figure]] = []
        self.you_loose: bool = False
        self.frame_counter: int = 0
        self.action: str = ''
        self.rows_to_remove = []
        self.speed: int = 10
        self.score: int = 0
        self.total_filled_rows: int = 0
        self.increase_speed = False

    # CYCLE CHECKPOINTS
    def speed_up(self) -> None:
        if self.total_filled_rows % FREQUENCY == 0 and self.increase_speed:
            self.increase_speed = False
            if self.speed < MAX_SPEED:
                self.speed += SPEED_GROWTH

    def switch_frame(self) -> bool:
        self.frame_counter += 1
        if self.frame_counter == COEFFICIENT // self.speed:
            self.frame_counter = 0
            return True
        return False

    def check_loss(self) -> None:
        for figure in self.all_figures[:-1]:
            for row, column in figure.coord:
                if row in (0, 1, 2):
                    self.you_loose = True
                    self.score = self.total_filled_rows * 1000
                    return

    # ACTIVE FIGURE
    def create_new_figure(self) -> None:
        if not self.next_figure:
            self.next_figure = random.choice((Tetris('green'),
                                              Origami('red'),
                                              Paw('violet'),
                                              Rectangle('yellow'),
                                              Angle('blue'),
                                              ReverseOrigami('orange'),
                                              ReverseAngle('pink')))

    def activate_figure(self) -> None:
        self.active_figure = copy(self.next_figure)
        self.all_figures.append(self.active_figure)
        self.next_figure = None

    def update_active_figure(self, game_loop) -> None:
        if self.active_figure:
            coord_to_try = [[row + FALL_COORD[0], column] for row, column in self.active_figure.find_coord()]
            if not is_figure_within_field(coord_to_try) or is_intersection(game_loop, coord_to_try):
                self.active_figure = None
                return
            self.active_figure.anchor_coord[0] += FALL_COORD[0]
            self.active_figure.coord = self.active_figure.find_coord()

    # REMOVE ROWS
    def find_filled_rows(self) -> List[int]:
        self.rows_to_remove = []
        for row_num in range(1, FIELD_SIZE[0]):
            row_coord = []
            for figure in self.all_figures[:-1]:
                row_coord.extend([(row, column) for row, column in figure.coord if row == row_num])
            if len(set(row_coord)) == FIELD_SIZE[1]:
                self.rows_to_remove.append(row_num)
                self.increase_speed = True
        if len(self.rows_to_remove) > 0:
            self.total_filled_rows += len(self.rows_to_remove)
        return self.rows_to_remove

    def remove_filled_rows(self) -> None:
        # remove filled row
        coord_to_remove = [[row, column] for column in range(FIELD_SIZE[1]) for row in self.rows_to_remove]
        for figure in self.all_figures:
            for coord in coord_to_remove:
                if coord in figure.coord:
                    figure.coord.remove(coord)
        # filter empty figures
        self.all_figures = [figure for figure in self.all_figures if figure.coord]
        self.shift_upper_rows(self.rows_to_remove)

    def shift_upper_rows(self, row_to_remove: List[List[int]]) -> None:
        for figure in self.all_figures[:-1]:
            for pair_num in range(len(figure.coord)):
                if figure.coord[pair_num][0] < row_to_remove[0]:
                    figure.coord[pair_num][0] += len(row_to_remove)
