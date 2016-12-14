from tkinter import Frame, Label, StringVar, Radiobutton, OptionMenu
from misc import Enigma1

ring_labels = Enigma1.labels


class BaseSlot(Frame):
    def __init__(self, master, text, tk_master=None, *args, **kwargs):
        tk_master = tk_master if tk_master else master
        Frame.__init__(self, tk_master, bd=1, relief='raised', *args, **kwargs)

        Label(self, text=text, bd=1, relief='sunken').pack(side='top', padx=5,
                                                           pady=5)

        self.master = master
        self.choice_var = StringVar()
        self.radio_group = []

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

    def update_selected(self, event=None):
        """
        Updates the master buffer
        :param event: Callback event handling
        """
        self.master.update_all()

    def update_available(self, type, event=None):
        for radio in self.radio_group:
            if radio['value'] == type:
                if radio['value'] != self.choice_var.get():
                    radio.config(state='disabled')
            else:
                radio.config(state='active')


class RotorSlot(BaseSlot):
    def __init__(self, master, index, tk_master=None, *args, **kwargs):
        text = ('THIRD', 'SECOND', 'FIRST')[index] + ' ROTOR'

        BaseSlot.__init__(self, master, text, tk_master, *args, **kwargs)

        self.index = index

        items = []
        items.extend(list(Enigma1.rotors.keys()))
        self.generate_contents(items)

        # Ring setting indicator
        self.ring_var = StringVar()

        Label(self, text='RING\nSETTING', bd=1, relief='sunken').pack(
            side='top', fill='x', padx=4)
        OptionMenu(self, self.ring_var, *ring_labels).pack(side='top')

        setting_idx = self.master.enigma.rotors[index].ring_setting
        curr_setting = ring_labels[setting_idx]
        self.ring_var.set(curr_setting)

        self.choice_var.set(self.master.enigma.rotors[index].get_label())
        self.ring_var.trace('w', self.update_selected)

    def update_selected(self, event=None):
        self.master.curr_rotors[self.index] = self.choice_var.get()
        ring_setting = Enigma1.labels.index(self.ring_var.get())
        self.master.curr_ring_settings[self.index] = ring_setting

        BaseSlot.update_selected(self)

    def update_available(self, event=None):
        BaseSlot.update_available(type=self.master.curr_rotors)


class ReflectorSlot(BaseSlot):
    def __init__(self, master, tk_master=None, *args, **kwargs):
        BaseSlot.__init__(self, master, 'REFLECTOR', tk_master, *args, **kwargs)

        items = []
        items.extend(list(Enigma1.reflectors.keys()))
        self.generate_contents(items)
        self.choice_var.set(self.master.enigma.reflector.get_label())

    def update_selected(self, event=None):
        self.master.curr_reflector = self.choice_var.get()

        BaseSlot.update_selected(self)

    def update_available(self, event=None):
        BaseSlot.update_available(type=self.master.curr_reflector)
