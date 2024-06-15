import time
from tkinter import *

from main_field import MainField


def main():
    root = Tk()
    root.geometry("1000x1000")
    MainField(root)
    time.sleep(0.4)
    root.mainloop()


if __name__ == '__main__':
    main()
