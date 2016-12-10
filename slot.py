from tkinter import Frame, Label, StringVar, Radiobutton, OptionMenu
from misc import Enigma1

ring_labels = Enigma1.labels

class Slot(Frame):
    def __init__(self, tk_master, master, enigma_instance, index=0, kind='rotor', *args, **kwargs):
        Frame.__init__(self, tk_master, bd=1, relief='raised', *args, **kwargs)

        labels = ('THIRD', 'SECOND', 'FIRST')

        self.master = master
        self.index = index
        self.kind = kind

        text = ''

        if kind == 'rotor':
            text = labels[index] + ' ROTOR'
        elif kind == 'reflector':
            text = 'REFLECTOR'

        Label(self, text=text, bd=1, relief='sunken').pack(side='top', padx=5, pady=5)

        self.enigma = enigma_instance
        self.choice_var = StringVar()
        self.socket_idx = 0
        self.radio_group = []

        items = []
        if kind == 'rotor':
            items.extend(list(Enigma1.rotors.keys()))
            self.generate_contents(items)
            self.socket_idx += 1

            # Ring setting indicator
            self.ring_var = StringVar()

            Label(self, text='RING\nSETTING', bd=1, relief='sunken').pack(side='top', fill='x', padx=4)

            OptionMenu(self, self.ring_var, *ring_labels).pack(side='top')

            setting_idx = self.enigma.rotors[index].ring_setting
            curr_setting = ring_labels[setting_idx]
            self.ring_var.set(curr_setting)

            self.choice_var.set(self.enigma.rotors[index].get_label())

            self.ring_var.trace('w', self.update_selected)

        elif kind == 'reflector':
            items.extend(list(Enigma1.reflectors.keys()))
            self.generate_contents(items)
            self.choice_var.set(self.enigma.reflector.get_label())

        self.choice_var.trace('w', self.update_selected)

        self.update_selected()

    def generate_contents(self, contents):
        for item in contents:
            radio = Radiobutton(self, text=item, variable=self.choice_var, value=item)
            radio.pack(side='top')
            self.radio_group.append(radio)

    def update_selected(self, *events):
        if self.kind == 'reflector':
            self.master.curr_reflector = self.choice_var.get()
        elif self.kind == 'rotor':
            self.master.curr_rotors[self.index] = self.choice_var.get()

            ring_setting = Enigma1.labels.index(self.ring_var.get())
            self.master.curr_ring_settings[self.index] = ring_setting

        # self.update_available()

    def update_available(self, *events):
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
