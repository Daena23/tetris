from figures import Block
from init_functions import initialize_game

def remove_layer(field, all_figures):
    bool_val = []
    line_to_remove = []
    # for row in range(FIELD_SIZE[0]):
    for line in field:
        for column in line:
            bool_val.append(line[column] == CELL_VALUE['Figure'])
            if all(bool_val):
                line_to_remove.append(field.index(line))
        bool_val = []
    coord_to_remove = []
    for figure in all_figures:
        for coord in figure.coord:
            if coord[0] == line_to_remove:
                coord_to_remove.append(coord)
    for coord in coord_to_remove:
        figure.coord.remove(coord)


init_field = initialize_game()
figure = Block()
all_figures = []
all_figures.append(figure)

print(init_field)



remove_layer(init_field, all_figures)