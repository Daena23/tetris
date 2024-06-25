from typing import List, Union

from configuration import FIELD_SIZE
from figures import Figure


def is_figure_within_field(coord_to_try: List[List[int]]) -> bool:
    return all([(0 <= row < FIELD_SIZE[0]) and (0 <= column <= FIELD_SIZE[1] - 1) for row, column in coord_to_try])


# SWITCH INDEXES
def switch_state_forward(figure: Figure) -> int:
    if figure.freedom_degree == 2:
        return (figure.state_index + 1) % 2
    else:
        if figure.state_index < 3:
            return figure.state_index + 1
        else:
            return 0


def switch_state_back(figure: Figure) -> int:
    if figure.freedom_degree == 2:
        return (figure.state_index + 1) % 2
    else:
        if figure.state_index > 0:
            return figure.state_index - 1
        else:
            return 3

