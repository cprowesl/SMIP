import tkinter as tk
from tkinter import ttk
from gui.Drawer import draw_menu

if __name__ == '__main__':
    root = tk.Tk()
    root.title("SMIP: The Student MIPS Instruction Program")
    # Turning off pack propagate to prevent widgets from determining window size.
    # Max and Min window sizes may change.
    root.pack_propagate(0)
    # Max size of window is the dimensions of their screen.
    their_width = root.winfo_screenwidth()
    their_height = root.winfo_screenheight()
    root.maxsize(their_width, their_height)
    # Buttons need room, so we need max height.
    root.minsize(700, their_height)
    # Put app at the center of the screen.
    x = (their_width / 2) - (700 / 2)
    y = (their_height / 2) - (800 / 2)
    root.geometry("%dx%d+%d+%d" % (700, 800, x, y))
    root.configure(background='medium blue')
    draw_menu(root, ttk)

    root.mainloop()
