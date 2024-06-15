from copy import deepcopy
from tkinter import Canvas
from typing import List, Optional

from PIL._tkinter_finder import tk

from auxillary_functions import create_new_figure, initialize_game, remove_cells
from configuration import CELL_VALUE, FALL_COORD, FIELD_SIZE, time_per_update, unit_size
from figures import Figure


class MainField:
    start_x, start_y = 1.25 * unit_size, unit_size
    hor_indent, vert_indent = unit_size / 4, unit_size / 4 + (FIELD_SIZE[1] + 1) * unit_size
    border_color = '#B6B6B6'

    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(bg="white",
                             height=(FIELD_SIZE[0] + 2) * unit_size,
                             width=(FIELD_SIZE[1] + 2.5) * unit_size)
        self.canvas.pack()
        self.draw_border(unit_size)
        # initial parameters
        self.init_field: List[List[int]] = initialize_game()
        self.field: Optional[List[List[int]]] = []
        self.active_figure: Optional[Figure] = None
        self.all_figures: Optional[List[Figure]] = []
        self.you_loose: bool = False
        self.frame_counter = 0
        # drawing
        self.canvas.bind_all("<KeyPress-Left>", self.step_left)
        # self.canvas.tag_bind("<KeyPress-Right>", self.move_right)
        # self.canvas.tag_bind("<KeyPress-Up>", self.move_up)
        # self.canvas.tag_bind("<KeyPress-Down>", self.move_down)
        self.root.after(20, self.update_game)

    def step_left(self, canvas):
        if self.active_figure:
        # todo condition to not наползать на другие фигуры
            if all(0 < column < FIELD_SIZE[1] for row, column in self.active_figure.find_coord()):
                print('123', self.active_figure)
                print(self.active_figure.coord, ' ', self.active_figure.anchor_coord)
                self.active_figure.anchor_coord[1] -= 1
                self.active_figure.coord = self.active_figure.find_coord()
                print(self.active_figure.coord, ' ', self.active_figure.anchor_coord)

    def switch_frame(self):
        self.frame_counter += 1
        if self.frame_counter == time_per_update:
            self.frame_counter = 0
            return True

    def update_game(self):
        if self.switch_frame():  # log
            self.reset_field()  # draw
            self.update_field()  # log
            if self.active_figure:
                self.update_active_figure()
            if not self.active_figure:
                if self.remove_filled_layers():
                    pass
                else:
                    self.active_figure = create_new_figure()
                    self.check_loss()
                    self.all_figures.append(self.active_figure)
            for figure in self.all_figures:  # draw
                self.draw_figure(figure)
            self.draw_upper_patch()  # draw
            if self.you_loose:
                self.draw_you_loose()
                return
            print()
            print('3', self.active_figure.coord, ' ', self.active_figure.anchor_coord)

        self.root.after(20, self.update_game)

    def update_field(self) -> None:
        self.field = deepcopy(self.init_field)
        if self.all_figures:
            for figure in self.all_figures:
                self.place_figure(figure)

    def place_figure(self, figure) -> None:
        for row, column in figure.coord:
            self.field[row][column] = CELL_VALUE[(figure.__repr__())]

    def remove_filled_layers(self):
        row_to_remove = self.find_filled_rows()
        coord_to_remove = [[row_num, cell_num] for cell_num in range(FIELD_SIZE[1]) for row_num in row_to_remove]
        for figure in self.all_figures:
            remove_cells(figure, coord_to_remove)
        return bool(coord_to_remove)

    def find_filled_rows(self) -> List[int]:
        row_to_remove = []
        for row_num in range(FIELD_SIZE[0]):
            if all([int(self.field[row_num][cell_num]) == 2 for cell_num in range(FIELD_SIZE[1])]):
                row_to_remove.append(row_num)
        return row_to_remove

    def check_loss(self):
        if self.active_figure:
            for row, column in self.active_figure.coord:
                if int(self.field[row][column]) == 2:  # int(CELL_VALUE[self.active_figure.__repr__()]):
                    self.you_loose = True
                    self.active_figure = None
                    return

    def update_active_figure(self):
        for row, column in self.active_figure.find_stuck_coord():
            if row < FIELD_SIZE[0] - 1:  # active figure falls on another figure
                if self.field[row + FALL_COORD[0]][column] != CELL_VALUE["Empty"]:
                    self.active_figure = None
                    return
            elif row == FIELD_SIZE[0] - 1:  # active figure falls on flour
                self.active_figure = None
                return
        self.active_figure.fall()

    def reset_field(self):
        self.canvas.create_rectangle(MainField.hor_indent + unit_size + 1,
                                     unit_size,
                                     MainField.hor_indent + (FIELD_SIZE[1] + 1) * unit_size - 1,
                                     FIELD_SIZE[0] * unit_size - 1, fill="white", outline="white")

    def draw_upper_patch(self):
        self.canvas.create_rectangle(MainField.hor_indent + 1 + unit_size,
                                     unit_size - 1,
                                     MainField.hor_indent - 1 + (FIELD_SIZE[1] + 1) * unit_size,
                                     2 * unit_size,
                                     fill="white", outline="white")
        self.draw_ceiling()

    def draw_you_loose(self):
        self.canvas.create_text(MainField.hor_indent + (FIELD_SIZE[1] + 2) * unit_size / 2,
                                (FIELD_SIZE[0] + 1.5) * unit_size,
                                text="You loose",
                                fill="black",
                                font=('Helvetica 15 bold'))

    def draw_ceiling(self):
        self.canvas.create_line(MainField.hor_indent,
                                2 * unit_size,
                                MainField.hor_indent + unit_size * (FIELD_SIZE[1] + 2),
                                2 * unit_size,
                                fill="black")

    def draw_figure(self, figure: Figure):
        tag = "fig"
        if figure:
            for coord in figure.coord:
                rect = self.canvas.create_rectangle(unit_size * (coord[1] - 1),
                                                    unit_size * (coord[0] - 1),
                                                    unit_size * (coord[1]),
                                                    unit_size * (coord[0]),
                                                    fill=f"{figure.color}", width=1.2, tags=f"{tag}")
                if figure is self.active_figure:
                   self.canvas.addtag_withtag("act_fig", "fig")
                # center_figure
                self.canvas.move(rect, MainField.start_x + unit_size, MainField.start_y)

    def move_figure(self, x, y):
        self.canvas.move("act_fig", x, y)

    def move_left(self, event):
        print('123')
        self.move_figure(-unit_size, 0)

    def move_right(self, event):
        self.move_figure(unit_size, 0)

    def move_up(self, event):
        self.move_figure(0, -unit_size)

    def move_down(self, event):
        self.move_figure(0, unit_size)

    def draw_border(self, unit_size):
        # vertical columns
        for indent in MainField.hor_indent, MainField.vert_indent:
            for unit_num in range(2, FIELD_SIZE[0] + 1):
                self.canvas.create_rectangle(indent,
                                             unit_num * unit_size,
                                             indent + unit_size,
                                             (unit_num + 1) * unit_size,
                                             fill=MainField.border_color
                                             )
        # horizontal columns
        for unit_num in range(FIELD_SIZE[1] + 2):
            rect = self.canvas.create_rectangle(MainField.hor_indent + unit_num * unit_size,
                                                FIELD_SIZE[0] * unit_size,
                                                MainField.hor_indent + (unit_num + 1) * unit_size,
                                                FIELD_SIZE[0] * unit_size + unit_size,
                                                fill=MainField.border_color
                                                )
        self.draw_ceiling()
