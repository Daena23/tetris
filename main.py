import time
from tkinter import *

from init_screen import Menu


def main():
    print('lupa')
    root = Tk()
    root.configure(background='#B6B6B6')
    root.geometry("800x800")
    Menu(root)
    time.sleep(0.4)
    root.mainloop()


if __name__ == '__main__':
    main()
