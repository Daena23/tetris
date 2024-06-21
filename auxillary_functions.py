from typing import List, Union

from configuration import CELL_VALUE, FIELD_SIZE
from figures import Figure


def initialize_game() -> List[List[int]]:
    return [[CELL_VALUE['Empty']] * FIELD_SIZE[1] for line_num in range(FIELD_SIZE[0])]


def remove_cells(figure: Figure, coord_to_remove: List[List[int]]) -> None:
    for coord in coord_to_remove:
        if coord in figure.coord:
            figure.coord.remove(coord)


def identify_figure(cell_value: Union[int, float]) -> Union[int, float]:
    for pair in (list(CELL_VALUE.items())):
        if cell_value in pair:
            return pair[0]


def is_border_contact(active_figure: Figure) -> bool:
    return any(row == FIELD_SIZE[0] for row, column in active_figure.find_coord())


# SWITCH INDEXES
def switch_state(figure):
    if figure.freedom_degree == 2:
        return (figure.state_index + 1) % 2
    else:
        if figure.state_index < 3:
            return figure.state_index + 1
        else:
            return 0


def switch_counterclockwise_four_states(figure):
    if figure.freedom_degree == 4:
        if figure.state_index > 0:
            return figure.state_index - 1
        else:
            return 3
