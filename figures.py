from abc import abstractmethod
from random import choice
from typing import List

from configuration import FALL_COORD, INIT_COORDINATES


class Figure:
    colors = ('red', 'blue', 'green', 'yellow', 'grey')

    def __init__(self):
        self.anchor_coord = list(INIT_COORDINATES)
        self.coord = self.find_coord()
        self.stuck_coord = self.find_stuck_coord()
        self.color = choice(Figure.colors)

    @property
    @abstractmethod
    def relative_coordinates(self) -> List[List[int]]:
        pass

    def find_coord(self) -> List[List[int]]:
        return [[row + self.anchor_coord[0],
                 column + self.anchor_coord[1]] for row, column in self.relative_coordinates]

    @property
    @abstractmethod
    def relative_stuck_coord(self) -> List[List[int]]:
        pass

    def find_stuck_coord(self) -> List[List[int]]:
        return [[row + self.anchor_coord[0],
                 column + self.anchor_coord[1]] for row, column in self.relative_stuck_coord]

    def fall(self) -> None:
        self.anchor_coord[0] += FALL_COORD[0]
        self.anchor_coord[1] += FALL_COORD[1]
        self.coord = self.find_coord()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}"


class Rectangle(Figure):
    @property
    def relative_coordinates(self) -> List[List[int]]:
        return [[0, 0], [0, 1],
                [1, 0], [1, 1]]

    @property
    def relative_stuck_coord(self) -> List[List[int]]:
        return [[row, column] for row, column in self.relative_coordinates
                if [row + FALL_COORD[0], column] not in self.relative_coordinates]

    def __init__(self):
        super().__init__()


class Tetris(Figure):
    @property
    def relative_coordinates(self) -> List[List[int]]:
        return [[0, 0], [0, 1], [0, 2], [0, 3]]

    @property
    def relative_stuck_coord(self) -> List[List[int]]:
        return [[row, column] for row, column in self.relative_coordinates
                if [row + FALL_COORD[0], column] not in self.relative_coordinates]

    def __init__(self):
        super().__init__()


class Angle(Figure):
    @property
    def relative_coordinates(self) -> List[List[int]]:
        return [[0, 0], [0, 1], [0, 2], [1, 2]]

    @property
    def relative_stuck_coord(self) -> List[List[int]]:
        return [[row, column] for row, column in self.relative_coordinates
                if [row + FALL_COORD[0], column] not in self.relative_coordinates]

    def __init__(self):
        super().__init__()


class Block(Figure):
    @property
    def relative_coordinates(self) -> List[List[int]]:
        return [[0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
                [1, -2], [1, -1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4]]

    @property
    def relative_stuck_coord(self) -> List[List[int]]:
        return [[row, column] for row, column in self.relative_coordinates
                if [row + FALL_COORD[0], column] not in self.relative_coordinates]

    def __init__(self):
        super().__init__()
