from typing import List

from configuration import FIELD_SIZE
from figures import Figure


def is_figure_within_field(coord_to_try: List[List[int]]) -> bool:
    return all([(0 <= row < FIELD_SIZE[0]) and (0 <= column <= FIELD_SIZE[1] - 1) for row, column in coord_to_try])


def is_intersection(game_loop, coord_to_try: List[List[int]]):
    for row, column in coord_to_try:
        for figure in game_loop.all_figures[:-1]:
            if [row, column] in figure.coord:
                return True
    return False

# SWITCH INDEXES
def switch_forward(figure: Figure) -> int:
    if figure.freedom_degree == 2:
        return (figure.state_index + 1) % 2
    else:
        if figure.state_index < 3:
            return figure.state_index + 1
        else:
            return 0


def switch_back(figure: Figure) -> int:
    if figure.freedom_degree == 2:
        return (figure.state_index + 1) % 2
    else:
        if figure.state_index > 0:
            return figure.state_index - 1
        else:
            return 3
