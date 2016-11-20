from os import path
from tkinter import Toplevel, Frame, Radiobutton, Label, StringVar, Button


def get_icon(icon):
    return path.join('icons', icon)


class RotorMenu(Toplevel):
    def __init__(self, curr_rotors, *args, **kwargs):
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
        self.root_frame = Frame(self)
        button_frame = Frame(self)
        self.rotor_frames = \
            [Frame(self.root_frame, bd=1, relief='raised', bg='gray85'),
             Frame(self.root_frame, bd=1, relief='raised', bg='gray85'),
             Frame(self.root_frame, bd=1, relief='raised', bg='gray85'),
             Frame(self.root_frame, bd=1, relief='raised', bg='gray85')]

        # Button
        Button(button_frame, text='Apply', command=self.get_values,
               width=12, bg='gray85').pack(side='right', padx=5, pady=5)

        # Rotor stash
        self.rotor_vars = [StringVar(), StringVar(), StringVar(),
                           StringVar()]  # UKW, I, II, III

        # Rotor nums
        self.radio_groups = [[], [], [], []]

        # Rotors
        rotors = ['I', 'II', 'III', 'IV', 'V', 'UKW-A', 'UKW-B', 'UKW-C']
        rotors = [[val] * 2 for val in rotors]

        # Reflectors
        Label(self.rotor_frames[0], text='REFLECTOR', bg='gray85', bd=1,
              relief='sunken').pack(side='top', pady=5, padx=5)
        for rotor, val in rotors[5:]:
            radio = Radiobutton(self.rotor_frames[0], text=rotor,
                                variable=self.rotor_vars[0], value=val,
                                bg='gray85')
            self.radio_groups[0].append(radio)

        # Rotors
        index = 1
        labels = [txt + ' ROTOR' for txt in ['THIRD', 'SECOND', 'FIRST']]
        for _ in self.rotor_frames[1:]:
            Label(self.rotor_frames[index], text=labels[index - 1], bg='gray85',
                  bd=1,
                  relief='sunken').pack(side='top', pady=5, padx=5)

            for rotor, val in rotors[:5]:
                radio = Radiobutton(self.rotor_frames[index], text=rotor,
                                    variable=self.rotor_vars[index], value=val,
                                    bg='gray85')
                self.radio_groups[index].append(radio)
            index += 1

        index = 0
        for values in self.radio_groups:
            for radio in values:
                radio.pack(side='top')
                text = radio.config()['text'][4]
                if text == curr_rotors[index]:
                    radio.select()
            index += 1

        # [rotor.pack(side='top') for rotor in radios]

        # Init
        [frame.pack(side='left', fill='both', padx=2) for frame in
         self.rotor_frames]
        button_frame.pack(side='bottom', fill='both')
        self.root_frame.pack(padx=10, pady=5)

    def get_values(self, event=None):
        return [test.get() for test in self.rotor_vars]
