from tkinter import *

from main_field import MainLoop


class Menu:
    def __init__(self, root):
        self.root = root
        self.game_type = None
        self.load_game = False
        self.init_screen()

    def init_screen(self):
        self.button_a = Button(self.root, text='A-type', command=self.button_a_clicked, bg='blue', padx=100, pady=30)
        self.button_b = Button(self.root, text='B-type', command=self.button_b_clicked, padx=100, pady=30)
        self.button_a.pack(side=LEFT, padx=90, pady=0)
        self.button_b.pack(side=LEFT, padx=50, pady=130)

    def button_a_clicked(self):
        self.game_type = 'A'
        self.activate_main_loop()

    def button_b_clicked(self):
        self.game_type = 'B'
        self.activate_main_loop()

    def activate_main_loop(self):
        self.button_a.destroy()
        self.button_b.destroy()
        MainLoop(self.root, self.game_type)
