from os import path
from tkinter import Toplevel, Frame, IntVar, Radiobutton, Label


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
        self.rotor_frames = \
            [Frame(self, bd=1, relief='raised', bg='gray85'),
             Frame(self, bd=1, relief='raised', bg='gray85'),
             Frame(self, bd=1, relief='raised', bg='gray85'),
             Frame(self, bd=1, relief='raised', bg='gray85')]

        # Rotor stash
        self.rotor_vars = [IntVar(), IntVar(), IntVar(),
                           IntVar()]  # UKW, I, II, III

        # Rotors
        rotors = ['I', 'II', 'III', 'IV', 'V', 'UKW-A', 'UKW-B', 'UKW-C']
        rotors = [[val] * 2 for val in rotors]

        # Reflectors
        Label(self.rotor_frames[0], text='REFLECTOR', bg='gray85', bd=1,
              relief='sunken').pack(side='top', pady=5, padx=5)
        for rotor, val in rotors[5:]:
            Radiobutton(self.rotor_frames[0], text=rotor,
                        variable=self.rotor_vars[0], value=val,
                        bg='gray85').pack(side='top')

        # Rotors
        index = 1
        labels = [txt + ' ROTOR' for txt in ['FIRST', 'SECOND', 'THIRD']]
        for _ in self.rotor_frames[1:]:
            Label(self.rotor_frames[index], text=labels[index - 1], bg='gray85',
                  bd=1,
                  relief='sunken').pack(side='top', pady=5, padx=5)

            for rotor, val in rotors[:5]:
                Radiobutton(self.rotor_frames[index], text=rotor,
                            variable=self.rotor_vars[index], value=val,
                            bg='gray85').pack(side='top')
            index += 1

        # Init
        [frame.pack(side='left') for frame in self.rotor_frames]

        self.update_menus()

    def update_menus(self):
        pass
