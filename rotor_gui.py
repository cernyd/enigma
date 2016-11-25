from os import path
from tkinter import Toplevel, Frame, Radiobutton, Label, StringVar, Button, OptionMenu
from misc import Enigma1, get_icon


ring_labels = Enigma1.labels


class RotorMenu(Toplevel):
    """GUI for setting rotor order, reflectors and ring settings"""
    def __init__(self, curr_rotors, ring_settings, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.curr_rotors = curr_rotors

        self.config(bg='gray85')
        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Bindings
        self.bind('<Button-1>', self.checkup)

        # Window config
        self.grab_set()
        self.iconbitmap(get_icon('rotor.ico'))
        self.resizable(False, False)
        self.wm_title("Rotor order")

        # Frames
        self.root_frame = Frame(self)
        self.root_frame.config(bg='gray85')
        button_frame = Frame(self)
        button_frame.config(bg='gray85')
        self.rotor_frames = \
            [Frame(self.root_frame, bd=1, relief='raised'),
             Frame(self.root_frame, bd=1, relief='raised'),
             Frame(self.root_frame, bd=1, relief='raised'),
             Frame(self.root_frame, bd=1, relief='raised')]

        # Buttons

        self.apply_button = Button(button_frame, text='Apply',
                                   command=self.destroy,
                                   width=12)

        self.apply_button.pack(side='right', padx=5, pady=5)

        self.storno_button = Button(button_frame, text='Storno',
                                    command=self.storno,
                                    width=12)

        self.storno_button.pack(side='right', padx=5, pady=5)

        # Rotor stash
        self.rotor_vars = [StringVar(), StringVar(), StringVar(),
                           StringVar()]  # UKW, I, II, III



        self.ring_setting_indicators = []

        # Rotor nums
        self.radio_groups = [[], [], [], []]

        # Rotors
        rotors = ['I', 'II', 'III', 'IV', 'V' ]
        reflectors = ['UKW-A', 'UKW-B', 'UKW-C']

        # Reflectors
        Label(self.rotor_frames[0], text='REFLECTOR', bd=1,
              relief='sunken').pack(side='top', pady=5, padx=5)

        for reflector in reflectors:
            radio = Radiobutton(self.rotor_frames[0], text=reflector,
                                variable=self.rotor_vars[0], value=reflector)
            self.radio_groups[0].append(radio)

        # Rotors
        index = 1
        labels = [txt + ' ROTOR' for txt in ['THIRD', 'SECOND', 'FIRST']]

        self.ring_setting_vars = [StringVar(), StringVar(), StringVar()]

        ring_settings = [ring_labels[setting] for setting in ring_settings]

        [var.set(setting) for var, setting in zip(self.ring_setting_vars, ring_settings)]

        for _ in self.rotor_frames[1:]:
            Label(self.rotor_frames[index], text=labels[index - 1], bd=1,
                  relief='sunken').pack(side='top', pady=5, padx=5)

            self.ring_setting_indicators.append(OptionMenu(self.rotor_frames[index], self.ring_setting_vars[index-1], *ring_labels))

            for rotor in rotors:
                radio = Radiobutton(self.rotor_frames[index], text=rotor,
                                    variable=self.rotor_vars[index],
                                    value=rotor)
                self.radio_groups[index].append(radio)

            index += 1

        for values in self.radio_groups:
            for radio in values:
                radio.pack(side='top')

        index = 0
        for values in self.radio_groups:
            for radio in values:
                text = radio.config()['text'][4]
                if text == self.curr_rotors[index]:
                    radio.select()
            index += 1

        [indicator.pack(side='bottom', pady=(0,5)) for indicator in self.ring_setting_indicators]

        index=1
        for _ in self.rotor_frames[1:]:
            Label(self.rotor_frames[index], text='RING \nSETTING', relief='sunken',
                  bd='1', width=12).pack(side='bottom', pady=5, padx=5)
            index+=1

        self.checkup()

        [var.trace('w', self.checkup) for var in self.rotor_vars]

        # Init
        [frame.pack(side='left', fill='both', padx=2) for frame in
         self.rotor_frames]
        button_frame.pack(side='bottom', fill='both')
        self.root_frame.pack(padx=10, pady=5)

    def checkup(self, *args):
        """Checks if all settings are valid ( determines if the apply button should be enabled )"""
        self.update_current()
        self.update_selected()
        self.can_apply()

    def update_current(self):
        """Updates current selected rotors"""
        self.curr_rotors = self.get_rotors()

    def storno(self):
        """Resets all values and destroys the window"""
        self.rotor_vars = []
        self.ring_setting_vars = []
        self.destroy()

    def update_selected(self):
        """Updates what radiobuttons are active based on selected buttons"""
        index = 0
        for values in self.radio_groups:
            for radio in values:
                text = radio.config()['text'][4]
                if text in self.curr_rotors:
                    if text != self.curr_rotors[index]:
                        radio.config(state='disabled')
                else:
                    radio.config(state='active')
            index += 1

    def get_rotors(self):
        """Gets all rotor values"""
        return [radio.get() for radio in self.rotor_vars]

    def get_ring_settings(self):
        """Gets all ring settings"""
        return [ring_labels.index(setting.get()) for setting in self.ring_setting_vars[::-1]]

    def can_apply(self, event=None):
        """Sets the apply button to active or disabled based on criteria"""
        if all(self.get_rotors()):
            self.apply_button.config(state='active')
        else:
            self.apply_button.config(state='disabled')
