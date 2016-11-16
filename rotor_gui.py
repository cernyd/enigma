from os import path
from tkinter import Toplevel, Frame, OptionMenu, StringVar
from historical import Enigma1


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

        # Rotors
        self.rotors = Enigma1.rotors.keys()

        # Rotor stash
        var = StringVar(self.rotor_stash)
        var.set("I")

        self.first_rotor = OptionMenu(self.rotor_stash, var, "I")
        self.second_rotor = OptionMenu(self.rotor_stash, var, "II")
        self.third_rotor = OptionMenu(self.rotor_stash, var, "III")

        # Init
        self.first_rotor.pack(side='left')
        self.second_rotor.pack(side='left')
        self.third_rotor.pack(side='left')

        self.rotor_stash.pack()

        self.update_menus()

    def update_menus(self):
        pass
        x = self.first_rotor['menu']
        print(x.entrycget(0, 'label'))