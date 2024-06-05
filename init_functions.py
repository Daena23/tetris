from typing import List

from configuration import CELL_VALUE, FIELD_SIZE


def initialize_game() -> List[List[int]]:
    init_field = [[CELL_VALUE['Empty']] * FIELD_SIZE[1] for line_num in range(FIELD_SIZE[0])]
    # add_border_on_field(init_field)
    return init_field
