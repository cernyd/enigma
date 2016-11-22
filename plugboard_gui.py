from tkinter import Toplevel, Entry, Label
from os import path


def get_icon(icon):
    return path.join('icons', icon)


labels = ['A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06',
           'G-07', 'H-08', 'I-09', 'J-10','K-11', 'L-12',
           'M-13', 'N-14', 'O-15', 'P-16', 'Q-17', 'R-18',
           'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24',
           'Y-25','Z-26']


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
        self.iconbitmap(get_icon('rotor.ico'))
        self.resizable(False, False)
        self.wm_title("Plugboard")