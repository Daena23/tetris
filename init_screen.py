from tkinter import *
from typing import Optional

from main_loop import MainLoop


class InitScreen:
    def __init__(self, root):
        self.root = root
        self.game_type: Optional[str] = None
        self.button_a: Optional[Button] = None
        self.button_b: Optional[Button] = None
        self.show_init_screen()

    def show_init_screen(self) -> None:
        self.button_a = Button(self.root, text='A-type', command=self.button_a_clicked, bg='blue', padx=100, pady=30)
        self.button_b = Button(self.root, text='B-type', command=self.button_b_clicked, bg='magenta', padx=100, pady=30)
        self.button_a.pack(side=LEFT, padx=90, pady=0)
        self.button_b.pack(side=RIGHT, padx=50, pady=130)

    def button_a_clicked(self) -> None:
        self.game_type = 'A'
        self.activate_main_loop()

    def button_b_clicked(self) -> None:
        self.game_type = 'B'
        self.activate_main_loop()

    def activate_main_loop(self) -> None:
        self.button_a.destroy()
        self.button_b.destroy()
        MainLoop(self.root, self.game_type)
