from configuration import INIT_COORDINATES


class Figure:
    def __init__(self, color, coord=None):
        self.state_index = 0
        self.freedom_degree = 2
        self.color = color
        # coord
        self.rel_coord = []
        self.rel_coord_library = []
        self.anchor_coord = list(INIT_COORDINATES)
        self.coord = []

    def find_all_coord(self):
        self.rel_coord = self.rel_coord_library[0]
        self.coord = self.find_coord()

    def find_coord(self):
        self.coord = [[row + self.anchor_coord[0], column + self.anchor_coord[1]] for row, column in self.rel_coord]
        return self.coord

    @property
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}"


class Tetris(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.rel_coord_library = [
            [[0, -1], [0, 0], [0, 1], [0, 2]],
            [[-1, 0], [0, 0], [1, 0], [2, 0]]
        ]
        self.find_all_coord()


class Rectangle(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.freedom_degree = 1
        self.rel_coord_library = [
            [[-1, 0], [0, 0], [0, -1], [-1, -1]]
        ]
        self.find_all_coord()


class Origami(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.rel_coord_library = [
            [[0, -1], [0, 0], [1, 0], [1, 1]],
            [[-1, 0], [0, 0], [0, -1], [1, -1]]
        ]
        self.find_all_coord()


class Angle(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.freedom_degree = 4
        self.rel_coord_library = [
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
        self.rel_coord_library = [
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
        self.rel_coord_library = [
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
        self.rel_coord_library = [
            [[1, 0], [0, 0], [0, 1], [1, -1]],
            [[1, 0], [0, 0], [0, -1], [-1, -1]],
        ]
        self.find_all_coord()


class NoodlesFigure(Figure):
    def __init__(self, color, coord):
        super().__init__(coord)
        self.coord = [coord]
        self.color = color
