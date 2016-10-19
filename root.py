from tkinter import Tk, Frame, Spinbox
from os import path


def get_icon(icon):
    return path.join('icons', icon)


class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Window config
        self.iconbitmap(get_icon('enigma.ico'))
        self.resizable(False, False)
        self.wm_title("Enigma")

        # Keybinds
        #self.bind('<Control-h>', None)
        #self.bind('<Control-l>', None)
        self.bind('<Key>', None)
        #self.bind('<Return>', None)

        # Frames
        self.rotor_container = Frame(self)
        self.io_container = Frame(self)
        self.plugboard = Frame(self)
        self.lid = Frame(self)

        # Rotor widgets
        self.left_rotor = Spinbox(self.rotor_container, width=10)
        self.mid_rotor = Spinbox(self.rotor_container, width=10)
        self.right_rotor = Spinbox(self.rotor_container, width=10)

        # Init
        self.left_rotor.grid(row=0, column=0)
        self.mid_rotor.grid(row=0, column=1)
        self.right_rotor.grid(row=0, column=2)

        self.rotor_container.pack()

test = Root()
test.mainloop()
