import random
from copy import deepcopy
from typing import List, Optional, Union

from configuration import CELL_VALUE, FALL_COORD, FIELD_SIZE
from figures import Angle, Figure, Rectangle, Tetris


# FIELD
def update_field(init_field: List[List[int]], all_figures: List[Figure]) -> List[List[int]]:
    field = deepcopy(init_field)
    for figure in all_figures:
        place_figure(field, figure)
    return field


def place_figure(field: List[List[int]], figure: Figure) -> None:
    if figure:
        for row, column in figure.coord:
            field[row][column] = CELL_VALUE[figure.__repr__()]


def identify_figure(cell_value: Union[int, float]) -> Union[int, float]:
    for pair in (list(CELL_VALUE.items())):
        if cell_value in pair:
            return pair[0]


def visualize(field: List[List[int]]) -> None:
    for line_num in range(FIELD_SIZE[0]):
        if line_num == 1:  # add a condition - if the figure is two-tiered
            continue
        print(line_num, end=' ')
        for cell in field[line_num]:
            if cell == CELL_VALUE['Empty']:
                print(' ', end='  ')
            elif cell == CELL_VALUE['Border']:
                print('□', end='  ')
            # elif cell == int(CELL_VALUE['FIGURE']):
            else:
                if identify_figure(cell) == 'Tetris':  # Figure.repr()
                    print('⮟', end='  ')
                else:
                    print('■', end='  ')
        print()


def update_active_figure(field: List[List[int]], active_figure: Figure) -> Optional[Figure]:
    for row, column in active_figure.find_stuck_coord():
        if field[row + FALL_COORD[0]][column] != CELL_VALUE["Empty"]:
            return None
    active_figure.fall()
    return active_figure


def create_new_figure() -> Figure:
    return random.choice((Rectangle(), Tetris(), Angle()))


def check_loss(field: List[List[int]], active_figure: Figure) -> bool:
    for row, column in active_figure.coord:
        if field[row][column] == CELL_VALUE['Figure']:
            return True
    return False
