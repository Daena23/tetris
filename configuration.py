FIELD_SIZE = (16, 8)  # width must be >= 6
CELL_VALUE = {'Empty': 0,
              'Border': 1,
              'Any_Fig': 2,
              'Tetris': 2.1,
              'Rectangle': 2.2,
              'Angle': 2.3,
              'ReverseAngle': 2.4,
              'Paw': 2.5,
              'Origami': 2.6,
              'ReverseOrigami': 2.7}

Paw_coord = [
            [[-1, 0], [0, 0], [1, 0], [0, 1]],
            [[0, 1], [0, 0], [1, 0], [0, -1]],
            [[-1, 0], [0, 0], [1, 0], [0, -1]],
            [[0, -1], [0, 0], [0, 1], [-1, 0]]
            ]

Tetris_coord = [
    [[0, -1], [0, 0], [0, 1], [0, 2]],
    [[-1, 0], [0, 0], [1, 0], [2, 0]]
    ]

Rectangle_coord = [
    [[-1, 1], [-1, 2], [0, 1], [0, 2]]
    ]

Origami_coord = [
    [[0, -1], [0, 0], [1, 0], [1, 1]],
    [[-1, 0], [0, 0], [0, -1], [1, -1]]
                ]

ReverseOrigami_coord = [
    [[1, 0], [0, 0], [0, 1], [1, -1]],
    [[1, 0], [0, 0], [0, -1], [-1, -1]],
                ]


Angle_coord = [[[0, 1], [0, 0], [1, 0], [2, 0]],
               [[1, 0], [0, 0], [0, -1], [0, -2]],
               [[0, -1], [0, 0], [-1, 0], [-2, 0]],
               [[-1, 0], [0, 0], [0, 1], [0, 2]]
               ]

ReverseAngle_coord = [
                     [[0, -1], [0, 0], [1, 0], [2, 0]],
                     [[-1, 0], [0, 0], [0, -1], [0, -2]],
                     [[0, 1], [0, 0], [-1, 0], [-2, 0]],
                     [[1, 0], [0, 0], [0, 1], [0, 2]]
                    ]

relative_coords_library = {'Tetris': Tetris_coord,
                           'Rectangle': Rectangle_coord,
                           'Angle': Angle_coord,
                           'Origami': Origami_coord,
                           'Paw': Paw_coord,
                           'ReverseAngle': ReverseAngle_coord,
                           'ReverseOrigami': ReverseOrigami_coord,
                           }


INIT_COORDINATES = (1, int(FIELD_SIZE[1] / 2) - 2)
FALL_COORD = (1, 0)
STEP_LEFT_COORD = (0, -1)
STEP_RIGHT_COORD = (0, 1)
INV_FALL_COORD = (1, 0)

unit_size = 30
frame_ms = 40
init_time_per_update = 12  # [2, 12]
