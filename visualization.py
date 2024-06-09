from tkinter import *
from configuration import FIELD_SIZE, unit_size


def draw_border(canvas, unit_size):
    marginal_indentation = 0.5 * unit_size / 2
    indents = (marginal_indentation,
               marginal_indentation + (FIELD_SIZE[1] + 1) * unit_size)
    # vertical columns
    for indent in indents:
        for unit_num in range(1, FIELD_SIZE[0] + 1):
            canvas.create_rectangle(indent,
                                    unit_num * unit_size,
                                    indent + unit_size,
                                    (unit_num + 1) * unit_size)

    # horizontal columns
    for unit_num in range(FIELD_SIZE[1] + 2):
        rect = canvas.create_rectangle(indents[0] + unit_num * unit_size,
                                FIELD_SIZE[0] * unit_size,
                                indents[0] + (unit_num + 1) * unit_size,
                                FIELD_SIZE[0] * unit_size + unit_size)


class Sketch:
    starting_point = (1.25 * unit_size, unit_size)

    def __init__(self, canvas, figure):
        self.items = []
        # self.canvas_center = (0.5 * unit_size / 2 + int(FIELD_SIZE[1] / 2) * unit_size, unit_size)
        self.canvas = canvas
        # figure.coord = [[9, 3], [9, 4], [9, 5], [9, 6]]
        self.items = [self.canvas.create_rectangle(unit_size * (coord[1] - 1),
                                                   unit_size * (coord[0] - 1),
                                                   unit_size * (coord[1]),
                                                   unit_size * (coord[0]), fill="blue") for coord in figure.coord]
        self.canvas.bind_all(self.center_figure())
        coords = [self.canvas.coords(item) for item in self.items]
        print(coords)
        # for figure in all_figures:
        #     if figure is active_figure:

        for coord in coords:
            if coord[0] > 62.5:  # < 462.5 and 50 < coord[1] < 600:
                self.canvas.bind_all("<KeyPress-Left>", self.move_left)
                self.canvas.bind_all("<KeyPress-Right>", self.move_right)
                self.canvas.bind_all("<KeyPress-Up>", self.move_up)
                self.canvas.bind_all("<KeyPress-Down>", self.move_down)

    def center_figure(self):
        for item in self.items:
            self.canvas.move(item, Sketch.starting_point[0], Sketch.starting_point[1])

    def move_left(self, event):
        self.move(-10, 0)

    def move_right(self, event):
        self.move(10, 0)

    def move_up(self, event):
        self.move(0, -10)

    def move_down(self, event):
        self.move(0, 10)

    def move(self, x, y):
        for item in self.items:
            self.canvas.move(item, x, y)


def visualize(all_figures):
    root = Tk()
    root.geometry("1000x1000")
    canvas = Canvas(bg="white",
                    height=(FIELD_SIZE[0] + 2) * unit_size,
                    width=(FIELD_SIZE[1] + 2.5) * unit_size)
    canvas.pack()
    # canvas_size = ((FIELD_SIZE[0] + 1) * unit_size, (FIELD_SIZE[1] + 2) * unit_size)
    draw_border(canvas, unit_size)
    for figure in all_figures:
        fig_on_field = Sketch(canvas, figure)
    root.mainloop()
