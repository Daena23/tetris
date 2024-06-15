import random
import time
from typing import List, Union

from configuration import CELL_VALUE, FIELD_SIZE
from figures import Angle, Block, Figure, Rectangle, Tetris


def initialize_game() -> List[List[int]]:
    return [[CELL_VALUE['Empty']] * FIELD_SIZE[1] for line_num in range(FIELD_SIZE[0])]


def identify_figure(cell_value: Union[int, float]) -> Union[int, float]:
    for pair in (list(CELL_VALUE.items())):
        if cell_value in pair:
            return pair[0]


def is_border_contact(active_figure):
    for row, column in active_figure.find_coord():
        if row == FIELD_SIZE[0]:
            return True
    return False


def create_new_figure() -> Figure:
    return random.choice((Rectangle(), Tetris(), Angle()))  # Block()


def remove_cells(figure: Figure, coord_to_remove: List[List[int]]) -> None:
    for coord in coord_to_remove:
        if coord in figure.coord:
            figure.coord.remove(coord)
