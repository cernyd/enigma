from os import path
from tkinter import Toplevel, Frame


def get_icon(icon):
    return path.join('icons', icon)

class RotorMenu(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Window config
        self.iconbitmap(get_icon(
            'rotor.ico'))  # Git push and add new files ( including icons! )
        self.resizable(False, False)
        self.wm_title("Rotor order")

        # Frames
        self.rotor_stash = Frame(self)
