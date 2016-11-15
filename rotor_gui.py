from os import path
from tkinter import Toplevel, Frame, OptionMenu, StringVar


def get_icon(icon):
    return path.join('icons', icon)

class RotorMenu(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Window config
        self.grab_set()
        self.iconbitmap(get_icon('rotor.ico'))
        self.resizable(False, False)
        self.wm_title("Rotor order")

        # Frames
        self.rotor_stash = Frame(self)

        # Rotor stash
        var = StringVar(self.rotor_stash)
        var.set("one")

        self.first_rotor = OptionMenu(self.rotor_stash, var, "one")
        self.second_rotor = OptionMenu(self.rotor_stash, var, "one")
        self.third_rotor = OptionMenu(self.rotor_stash, var, "one")

        # Init
        self.first_rotor.pack()
        self.second_rotor.pack()
        self.third_rotor.pack()

        self.rotor_stash.pack()
