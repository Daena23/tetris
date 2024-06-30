# # menu
# from functools import partial
# from configuration import FIELD_SIZE, UNIT_SIZE
#
#
# def button_clicked(root):
#     root.destroy()
#     canvas = Canvas(bg="white",
#                     height=(FIELD_SIZE[0] + 3.5) * UNIT_SIZE,
#                     width=(FIELD_SIZE[1] + 9) * UNIT_SIZE)
#     canvas.pack()
#     for indent in (1, 1):
#         for unit_num in range(2, FIELD_SIZE[0] + 1):
#             canvas.create_rectangle(indent,
#                                          unit_num * UNIT_SIZE,
#                                          indent + UNIT_SIZE,
#                                          (unit_num + 1) * UNIT_SIZE,
#                                          fill='blue'
#                                          )
#             canvas.pack()
#
from tkinter import *


def remove_widget(widget):
    widget.place_forget()


root = Tk()
root.geometry("800x800")
button_a = Button(root, text='A-type', bg='blue', padx=100, pady=30)
button_b = Button(root, text='B-type', padx=100, pady=30)
button_a.pack()
button_b.pack()
button_a.destroy()
root.mainloop()

# button_A = Button(root, text='A-type', command=partial(button_clicked, root), bg='blue', padx=100, pady=30)
# button_B = Button(root, text='B-type', padx=100, pady=30)
#
# button_A.grid(row=0, column=0, sticky=W, padx=100, pady=200)
# button_B.grid(row=0, column=1, sticky=W)
#
# root.mainloop()
