from tkinter import Toplevel, Entry, Label
from os import path
from historical import Enigma1


def get_icon(icon):
    return path.join('icons', icon)


labels = Enigma1.labels


class PlugboardMenu(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.config(bg='gray85')
        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Bindings
        self.bind('<Button-1>', None)

        # Window config
        self.grab_set()
        self.iconbitmap(get_icon('plugboard.ico'))
        self.resizable(False, False)
        self.wm_title("Plugboard")