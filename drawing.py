from configuration import FIELD_SIZE, UNIT_SIZE
from figures import Figure


class Draw:
    start_x, start_y = 1.25 * UNIT_SIZE, UNIT_SIZE
    hor_indent, vert_indent = UNIT_SIZE / 4, UNIT_SIZE / 4 + (FIELD_SIZE[1] + 1) * UNIT_SIZE
    border_color = '#B6B6B6'

    def __init__(self, canvas):
        self.canvas = canvas

    def update_canvas(self, game_loop) -> None:
        self.canvas.delete("all")
        self.border()
        future_fig = game_loop.next_figure
        self.empty_canvas()
        if future_fig:
            self.future_figure(future_fig)
        self.is_player_lost(game_loop)
        # self.empty_canvas()
        for figure in game_loop.all_figures:
            self.figure(figure)
        self.upper_patch()

    def empty_canvas(self) -> None:
        self.canvas.create_rectangle(Draw.hor_indent + UNIT_SIZE + 1,
                                     UNIT_SIZE,
                                     Draw.hor_indent + (FIELD_SIZE[1] + 1) * UNIT_SIZE - 1,
                                     FIELD_SIZE[0] * UNIT_SIZE - 1, fill="white", outline="white")

    def upper_patch(self) -> None:
        self.canvas.create_rectangle(UNIT_SIZE,
                                     0,
                                     Draw.hor_indent + (FIELD_SIZE[1] + 1) * UNIT_SIZE,
                                     2 * UNIT_SIZE,
                                     fill="white", outline="white")
        self.ceiling()

    def is_player_lost(self, game_loop) -> None:
        if game_loop.you_loose:
            self.canvas.create_text(Draw.hor_indent + (FIELD_SIZE[1] + 2) * UNIT_SIZE / 2,
                                    (FIELD_SIZE[0] + 1.7) * UNIT_SIZE,
                                    text="You loose",
                                    fill="black",
                                    font='Helvetica 15 bold')

            self.canvas.create_text(Draw.hor_indent + (FIELD_SIZE[1] + 2) * UNIT_SIZE / 2,
                                    (FIELD_SIZE[0] + 2.5) * UNIT_SIZE,
                                    text=f"Your score is {game_loop.score}",
                                    fill="black",
                                    font='Helvetica 13 bold')
            return game_loop.you_loose

    def ceiling(self) -> None:
        self.canvas.create_line(Draw.hor_indent,
                                2 * UNIT_SIZE,
                                Draw.hor_indent + UNIT_SIZE * (FIELD_SIZE[1] + 2),
                                2 * UNIT_SIZE,
                                fill="black")

    def future_figure(self, figure: Figure) -> None:
        self.canvas.create_rectangle(UNIT_SIZE * 12.5,
                                     UNIT_SIZE * 11,
                                     UNIT_SIZE * 19,
                                     UNIT_SIZE * 16,
                                     fill='white', outline='black', width=1.2)
        if figure:
            for coord in figure.rel_coord_library[0]:
                rect = self.canvas.create_rectangle(UNIT_SIZE * (coord[1] - 1),
                                                    UNIT_SIZE * (coord[0] - 1),
                                                    UNIT_SIZE * (coord[1]),
                                                    UNIT_SIZE * (coord[0]),
                                                    fill=f'{figure.color}', width=1.2)
                # center_figure,
                self.canvas.move(rect, UNIT_SIZE * 16, UNIT_SIZE * 13.5)

    def figure(self, figure: Figure) -> None:
        if figure:
            for coord in figure.coord:
                rect = self.canvas.create_rectangle(UNIT_SIZE * (coord[1] - 1),
                                                    UNIT_SIZE * (coord[0] - 1),
                                                    UNIT_SIZE * (coord[1]),
                                                    UNIT_SIZE * (coord[0]),
                                                    fill=f'{figure.color}', width=1.2)

                # center_figure
                self.canvas.move(rect, Draw.start_x + UNIT_SIZE, Draw.start_y)

    def border(self) -> None:
        # vertical columns
        for indent in (Draw.hor_indent, Draw.vert_indent):
            for unit_num in range(2, FIELD_SIZE[0] + 1):
                self.canvas.create_rectangle(indent,
                                             unit_num * UNIT_SIZE,
                                             indent + UNIT_SIZE,
                                             (unit_num + 1) * UNIT_SIZE,
                                             fill=Draw.border_color
                                             )

        # horizontal columns
        for unit_num in range(FIELD_SIZE[1] + 2):
            self.canvas.create_rectangle(Draw.hor_indent + unit_num * UNIT_SIZE,
                                         FIELD_SIZE[0] * UNIT_SIZE,
                                         Draw.hor_indent + (unit_num + 1) * UNIT_SIZE,
                                         FIELD_SIZE[0] * UNIT_SIZE + UNIT_SIZE,
                                         fill=Draw.border_color
                                         )
        self.ceiling()
