from configuration import FIELD_SIZE, unit_size
from figures import Figure


class Draw:
    start_x, start_y = 1.25 * unit_size, unit_size
    hor_indent, vert_indent = unit_size / 4, unit_size / 4 + (FIELD_SIZE[1] + 1) * unit_size
    border_color = '#B6B6B6'

    def __init__(self, canvas):
        self.canvas = canvas

    def update_canvas(self, game_loop) -> None:
        self.canvas.delete("all")
        self.border()
        self.is_player_lost(game_loop)
        self.empty_canvas()
        for figure in game_loop.all_figures:
            self.figure(figure)
        self.upper_patch()

    def empty_canvas(self) -> None:
        self.canvas.create_rectangle(Draw.hor_indent + unit_size + 1,
                                     unit_size,
                                     Draw.hor_indent + (FIELD_SIZE[1] + 1) * unit_size - 1,
                                     FIELD_SIZE[0] * unit_size - 1, fill="white", outline="white")

    def upper_patch(self) -> None:
        self.canvas.create_rectangle(unit_size,
                                     0,
                                     Draw.hor_indent + (FIELD_SIZE[1] + 1) * unit_size,
                                     2 * unit_size,
                                     fill="white", outline="white")
        self.ceiling()

    def is_player_lost(self, game_loop) -> None:
        if game_loop.you_loose:
            print('draw you_loose', game_loop.you_loose)
            self.canvas.create_text(Draw.hor_indent + (FIELD_SIZE[1] + 2) * unit_size / 2,
                                    (FIELD_SIZE[0] + 1.5) * unit_size,
                                    text="You loose",
                                    fill="black",
                                    font='Helvetica 15 bold')
            return game_loop.you_loose

    def ceiling(self) -> None:
        self.canvas.create_line(Draw.hor_indent,
                                2 * unit_size,
                                Draw.hor_indent + unit_size * (FIELD_SIZE[1] + 2),
                                2 * unit_size,
                                fill="black")

    def figure(self, figure: Figure) -> None:
        if figure:
            for coord in figure.coord:
                rect = self.canvas.create_rectangle(unit_size * (coord[1] - 1),
                                                    unit_size * (coord[0] - 1),
                                                    unit_size * (coord[1]),
                                                    unit_size * (coord[0]),
                                                    fill=f"{self.define_color(coord, figure)}", width=1.2)

                # center_figure
                self.canvas.move(rect, Draw.start_x + unit_size, Draw.start_y)

    def define_color(self, coord, figure):
        figure_color = figure.color
        return figure_color

    def border(self) -> None:
        # vertical columns
        for indent in (Draw.hor_indent, Draw.vert_indent):
            for unit_num in range(2, FIELD_SIZE[0] + 1):
                self.canvas.create_rectangle(indent,
                                             unit_num * unit_size,
                                             indent + unit_size,
                                             (unit_num + 1) * unit_size,
                                             fill=Draw.border_color
                                             )

        # horizontal columns
        for unit_num in range(FIELD_SIZE[1] + 2):
            self.canvas.create_rectangle(Draw.hor_indent + unit_num * unit_size,
                                         FIELD_SIZE[0] * unit_size,
                                         Draw.hor_indent + (unit_num + 1) * unit_size,
                                         FIELD_SIZE[0] * unit_size + unit_size,
                                         fill=Draw.border_color
                                         )
        self.ceiling()
