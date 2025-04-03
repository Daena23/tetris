from typing import List

from configuration import INIT_COORDINATES


class Figure:
    def __init__(self, color):
        self.state_index = 0
        self.freedom_degree = 2
        self.color = color
        # coord
        self.relative_coord = []
        self.relative_coord_library = []
        self.anchor_coord = list(INIT_COORDINATES)
        self.coord = []

    def find_all_coord(self) -> None:
        self.relative_coord = self.relative_coord_library[0]
        self.coord = self.find_coord()

    def find_coord(self) -> List[List[int]]:
        return [[row + self.anchor_coord[0], column + self.anchor_coord[1]] for row, column in self.relative_coord]

    @property
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}"


class Tetris(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.relative_coord_library = [
            [[0, -1], [0, 0], [0, 1], [0, 2]],
            [[-1, 0], [0, 0], [1, 0], [2, 0]]
        ]
        self.find_all_coord()


class Rectangle(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.freedom_degree = 1
        self.relative_coord_library = [
            [[-1, 0], [0, 0], [0, -1], [-1, -1]]
        ]
        self.find_all_coord()


class Origami(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.relative_coord_library = [
            [[0, -1], [0, 0], [1, 0], [1, 1]],
            [[-1, 0], [0, 0], [0, -1], [1, -1]]
        ]
        self.find_all_coord()


class Angle(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.freedom_degree: int = 4
        self.relative_coord_library = [
            [[1, 1], [0, 1], [0, 0], [0, -1]],
            [[-1, 1], [-1, 0], [0, 0], [1, 0]],
            [[-1, -1], [0, -1], [0, 0], [0, 1]],
            [[1, -1], [1, 0], [0, 0], [-1, 0]],
        ]
        self.find_all_coord()


class Paw(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.freedom_degree = 4
        self.relative_coord_library = [
            [[0, -1], [0, 0], [0, 1], [-1, 0]],
            [[1, 0], [0, 0], [-1, 0], [0, -1]],
            [[0, -1], [0, 0], [0, 1], [1, 0]],
            [[1, 0], [0, 0], [-1, 0], [0, 1]],
        ]
        self.find_all_coord()


class ReverseAngle(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.freedom_degree = 4
        self.relative_coord_library = [
            [[-1, 1], [0, 1], [0, 0], [0, -1]],
            [[-1, -1], [-1, 0], [0, 0], [1, 0]],
            [[1, -1], [0, -1], [0, 0], [0, 1]],
            [[1, 1], [1, 0], [0, 0], [-1, 0]],
        ]
        self.find_all_coord()


class ReverseOrigami(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.freedom_degree = 2
        self.relative_coord_library = [
            [[1, 0], [0, 0], [0, 1], [1, -1]],
            [[1, 0], [0, 0], [0, -1], [-1, -1]],
        ]
        self.find_all_coord()


class NoodlesFigure(Figure):
    def __init__(self, color, coord):
        super().__init__(coord)
        self.coord = [coord]
        self.color = color
