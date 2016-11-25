from tkinter import Toplevel, Entry, Label
from misc import Enigma1, get_icon


class PlugboardMenu(Toplevel):
    """GUI for visual plugboard pairing setup"""
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