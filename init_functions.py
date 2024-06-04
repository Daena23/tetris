from typing import List

from configuration import CELL_VALUE, FIELD_SIZE


def add_border_on_field(field: List[List[int]]) -> None:
    for row in range(FIELD_SIZE[0]):
        for column in range(FIELD_SIZE[1]):
            if row in (0, FIELD_SIZE[0] - 1) or column in (0, FIELD_SIZE[1] - 1):
                field[row][column] = 2


def initialize_game() -> List[List[int]]:
    init_field = [[CELL_VALUE['Empty']] * FIELD_SIZE[1] for line_num in range(FIELD_SIZE[0])]
    add_border_on_field(init_field)
    return init_field
