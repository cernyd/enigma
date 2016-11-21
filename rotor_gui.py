from os import path
from tkinter import Toplevel, Frame, Radiobutton, Label, StringVar, Button


def get_icon(icon):
    return path.join('icons', icon)


class RotorMenu(Toplevel):
    def __init__(self, curr_rotors, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.curr_rotors = curr_rotors

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Bindings
        self.bind('<Button>')

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

        # Buttons

        Button(button_frame, text='Apply', command=self.destroy,
               width=12, bg='gray85').pack(side='right', padx=5, pady=5)

        Button(button_frame, text='Storno', command=self.storno,
               width=12, bg='gray85').pack(side='right', padx=5, pady=5)

        # Rotor stash
        self.rotor_vars = [StringVar(), StringVar(), StringVar(),
                           StringVar()]  # UKW, I, II, III

        # Rotor nums
        self.radio_groups = [[], [], [], []]

        # Rotors
        rotors = ['I', 'II', 'III', 'IV', 'V' ]
        reflectors = ['UKW-A', 'UKW-B', 'UKW-C']

        # Reflectors
        Label(self.rotor_frames[0], text='REFLECTOR', bg='gray85', bd=1,
              relief='sunken').pack(side='top', pady=5, padx=5)
        for reflector in reflectors:
            radio = Radiobutton(self.rotor_frames[0], text=reflector,
                                variable=self.rotor_vars[0], value=reflector,
                                bg='gray85')
            self.radio_groups[0].append(radio)

        # Rotors
        index = 1
        labels = [txt + ' ROTOR' for txt in ['THIRD', 'SECOND', 'FIRST']]
        for _ in self.rotor_frames[1:]:
            Label(self.rotor_frames[index], text=labels[index - 1], bg='gray85',
                  bd=1,
                  relief='sunken').pack(side='top', pady=5, padx=5)

            for rotor in rotors:
                radio = Radiobutton(self.rotor_frames[index], text=rotor,
                                    variable=self.rotor_vars[index], value=rotor,
                                    bg='gray85')
                self.radio_groups[index].append(radio)
            index += 1

        for values in self.radio_groups:
            for radio in values:
                radio.pack(side='top')

        self.update_available()

        # Init
        [frame.pack(side='left', fill='both', padx=2) for frame in
         self.rotor_frames]
        button_frame.pack(side='bottom', fill='both')
        self.root_frame.pack(padx=10, pady=5)

    def update_current(self):
        self.curr_rotors = self.get_values()

    def storno(self):
        self.rotor_vars = []
        self.destroy()

    def update_available(self, event=None):  # Initial update
        index = 0
        for values in self.radio_groups:
            for radio in values:
                text = radio.config()['text'][4]
                if text == self.curr_rotors[index]:
                    radio.select()
            index += 1

    def update_selected(self, event=None):
        index = 0
        for values in self.radio_groups:
            for radio in values:
                text = radio.config()['text'][4]
                if not text == self.curr_rotors[index]:
                    if text in self.curr_rotors:
                        radio.config(state='disabled')
                    else:
                        radio.config(state='active')
            index += 1

    def get_values(self, event=None):
        return [test.get() for test in self.rotor_vars]
