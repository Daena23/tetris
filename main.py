import time
from typing import List, Optional

from figures import Figure
from game_loop import check_loss, create_new_figure, remove_filled_layers, update_active_figure, update_field, visualize
from init_functions import initialize_game


def main():
    # initial parameters
    init_field = initialize_game()
    # variables
    you_loose: bool = False
    active_figure: Optional[Figure] = None
    all_figures: List[Figure] = []
    while not you_loose:
        field = update_field(init_field, all_figures)
        visualize(field)
        if active_figure:
            active_figure = update_active_figure(field, active_figure)
        if not active_figure:
            if remove_filled_layers(field, all_figures):
                continue
            else:
                active_figure = create_new_figure()
                all_figures.append(active_figure)
                you_loose = check_loss(field, active_figure)

        print('--------')
        # game_iteration += 1
        time.sleep(0.4)
    print('You loose')


if __name__ == '__main__':
    main()
