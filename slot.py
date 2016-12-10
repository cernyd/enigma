from tkinter import Frame, Label, StringVar, Radiobutton, OptionMenu
from misc import Enigma1

ring_labels = Enigma1.labels

class Slot(Frame):
    """Customizable slot frame for setting rotor and ring settings"""
    def __init__(self, tk_master, master, index=0, kind='rotor', *args, **kwargs):
        # Superclass constructor call
        Frame.__init__(self, tk_master, bd=1, relief='raised', *args, **kwargs)

        # Config stuff
        labels = ('THIRD', 'SECOND', 'FIRST')
        text = ''

        if kind == 'rotor':
            text = labels[index] + ' ROTOR'
        elif kind == 'reflector':
            text = 'REFLECTOR'

        Label(self, text=text, bd=1, relief='sunken').pack(side='top', padx=5,
                                                           pady=5)

        # Master for editing enigma buffer and refreshing other slots
        self.master = master
        self.index = index
        self.kind = kind
        self.choice_var = StringVar()
        self.radio_group = []

        items = []
        if kind == 'rotor':
            items.extend(list(Enigma1.rotors.keys()))
            self.generate_contents(items)

            # Ring setting indicator
            self.ring_var = StringVar()

            Label(self, text='RING\nSETTING', bd=1, relief='sunken').pack(side='top', fill='x', padx=4)
            OptionMenu(self, self.ring_var, *ring_labels).pack(side='top')

            setting_idx = self.master.enigma.rotors[index].ring_setting
            curr_setting = ring_labels[setting_idx]
            self.ring_var.set(curr_setting)

            self.choice_var.set(self.master.enigma.rotors[index].get_label())
            self.ring_var.trace('w', self.update_selected)
        elif kind == 'reflector':
            items.extend(list(Enigma1.reflectors.keys()))
            self.generate_contents(items)
            self.choice_var.set(self.master.enigma.reflector.get_label())

        self.choice_var.trace('w', self.update_selected)
        self.update_selected()

    def generate_contents(self, contents):
        """
        :param contents: Contents to generate as tk radios
        """
        for item in contents:
            radio = Radiobutton(self, text=item, variable=self.choice_var, value=item)
            radio.pack(side='top')
            self.radio_group.append(radio)

    def update_selected(self, *events):
        """
        Updates the master buffer
        :param events: Callback event handling
        """
        if self.kind == 'reflector':
            self.master.curr_reflector = self.choice_var.get()
        elif self.kind == 'rotor':
            self.master.curr_rotors[self.index] = self.choice_var.get()

            ring_setting = Enigma1.labels.index(self.ring_var.get())
            self.master.curr_ring_settings[self.index] = ring_setting

        self.master.update_all()

    def update_available(self, *events):
        """

        :param events: Callback event handling
        """
        for radio in self.radio_group:
            if self.kind == 'reflector':
                if radio['value'] == self.master.curr_reflector:
                    if radio['value'] != self.choice_var.get():
                        radio.config(state='disabled')
                else:
                    radio.config(state='active')
            elif self.kind == 'rotor':
                if radio['value'] in self.master.curr_rotors:
                    if radio['value'] != self.choice_var.get():
                        radio.config(state='disabled')
                else:
                    radio.config(state='active')
