import tkinter as tk
from tkinter.constants import LEFT, RIGHT
import os
import sys

def load_ui():
    os.chdir(sys.path[0])

    win = tk.Tk()

    scroll_bar = tk.Scrollbar(win)
    scroll_bar.pack(side = RIGHT)

    mylist = tk.Listbox(win , yscrollcommand = scroll_bar.set)

    def act():
        try:
            with open("songs.txt" , "r") as f:
                songs = f.readlines()
            mylist.delete(0,tk.END)
            for song in songs:
                mylist.insert(tk.END,song)
            mylist.pack(side = LEFT)
            win.after(3,act)
        except FileNotFoundError:
            pass

    win.after(3,act)
    win.mainloop()


load_ui()