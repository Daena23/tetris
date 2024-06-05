import random
import time
from copy import deepcopy
from typing import List, Optional, Union

from configuration import CELL_VALUE, FALL_COORD, FIELD_SIZE
from figures import Angle, Block, Figure, Rectangle, Tetris


# FIELD
def update_field(init_field: List[List[int]], all_figures: List[Figure]) -> List[List[int]]:
    field = deepcopy(init_field)
    for figure in all_figures:
        place_figure(field, figure)
    return field


def place_figure(field: List[List[int]], figure: Figure) -> None:
    if figure:
        for row, column in figure.coord:
            field[row][column] = CELL_VALUE['Figure']


def identify_figure(cell_value: Union[int, float]) -> Union[int, float]:
    for pair in (list(CELL_VALUE.items())):
        if cell_value in pair:
            return pair[0]


def visualize(field: List[List[int]]) -> None:
    for line_num in range(FIELD_SIZE[0]):
        if line_num in (0, 1):  # add a condition - if the figure is two-tiered
            print()
            continue
        print('□', end=' ')
        print(' ', end='')
        for cell in field[line_num]:
            if cell == CELL_VALUE['Empty']:
                print('_', end='  ')
            else:
                if identify_figure(cell) == 'Tetris':  # Figure.repr()
                    print('⮟', end='  ')
                else:
                    print('■', end='  ')
        print('□')
    for cell_num in range(FIELD_SIZE[1] + 2):
        print('□', end='  ')
    print()


def is_border_contact(active_figure):
    for row, column in active_figure.find_coord():
        if row == FIELD_SIZE[0]:
            return True
    return False


def update_active_figure(field: List[List[int]], active_figure: Figure) -> Optional[Figure]:
    for row, column in active_figure.find_stuck_coord():
        if row < FIELD_SIZE[0] - 1:
            if field[row + FALL_COORD[0]][column] != CELL_VALUE["Empty"]:
                return None
        elif row == FIELD_SIZE[0] - 1:
            return None
    active_figure.fall()
    return active_figure


def create_new_figure() -> Figure:
    return random.choice((Rectangle(), Tetris(), Angle()))  # Block()


def check_loss(field: List[List[int]], active_figure: Figure) -> bool:
    for row, column in active_figure.coord:
        if field[row][column] == CELL_VALUE['Figure']:
            return True
    return False


def find_filled_rows(field: List[List[int]]) -> List[int]:
    row_to_remove = []
    for row_num in range(FIELD_SIZE[0]):
        if all([cell == CELL_VALUE['Figure'] for cell in field[row_num]]):
            row_to_remove.append(row_num)
    return row_to_remove


def remove_cells(figure: Figure, coord_to_remove: List[List[int]]) -> None:
    for coord in coord_to_remove:
        if coord in figure.coord:
            figure.coord.remove(coord)


def remove_filled_layers(field, all_figures):
    row_to_remove = find_filled_rows(field)
    coord_to_remove = [[row_num, cell_num] for cell_num in range(FIELD_SIZE[1]) for row_num in row_to_remove]
    for figure in all_figures:
        remove_cells(figure, coord_to_remove)
    time.sleep(0.6)
