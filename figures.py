from random import choice
from typing import List

from configuration import FALL_COORD, INIT_COORDINATES, relative_coords_library


class Figure:
    colors = ('red', 'blue', 'green', 'yellow', 'magenta', 'orange')

    def __init__(self):
        self.color = choice(Figure.colors)
        self.state_index = 0
        self.freedom_degree = 2
        # coord
        self.anchor_coord = list(INIT_COORDINATES)
        self.relative_coordinates = []
        self.coord = []
        self.stuck_coord = []

    def find_all_coord(self):
        self.find_init_relative_coord()
        self.find_coord()
        self.find_stuck_coord()

    def find_init_relative_coord(self):
        self.relative_coordinates = relative_coords_library[self.__repr__()][0]

    def find_coord(self) -> List[List[int]]:
        return [[row + self.anchor_coord[0], column + self.anchor_coord[1]] for row, column in self.relative_coordinates]

    @property
    def relative_stuck_coord(self) -> List[List[int]]:
        return [[row, column] for row, column in self.relative_coordinates
                if [row + FALL_COORD[0], column] not in self.relative_coordinates]

    def find_stuck_coord(self) -> List[List[int]]:
        return [[row + self.anchor_coord[0],
                 column + self.anchor_coord[1]] for row, column in self.relative_stuck_coord]

    def fall(self) -> None:
        self.anchor_coord[0] += FALL_COORD[0]
        self.coord = self.find_coord()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}"


class Tetris(Figure):
    def __init__(self):
        super().__init__()
        self.find_all_coord()


class Rectangle(Figure):
    def __init__(self):
        super().__init__()
        self.freedom_degree = 1
        self.find_all_coord()


class Origami(Figure):
    def __init__(self):
        super().__init__()
        self.find_all_coord()


class Angle(Figure):
    def __init__(self):
        super().__init__()
        self.freedom_degree = 4
        self.find_all_coord()


class Paw(Figure):
    def __init__(self):
        super().__init__()
        self.freedom_degree = 4
        self.find_all_coord()


class ReverseAngle(Figure):
    def __init__(self):
        super().__init__()
        self.freedom_degree = 4
        self.find_all_coord()


class ReverseOrigami(Figure):
    def __init__(self):
        super().__init__()
        self.freedom_degree = 2
        self.find_all_coord()
