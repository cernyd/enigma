from tkinter import Frame, Label, StringVar, Radiobutton, OptionMenu
from tkinter import Frame, Label, StringVar, Radiobutton, OptionMenu
from rotor_factory import DataStorage


labels = DataStorage.get_info('labels')


class BaseSlot(Frame):
    def __init__(self, master, text, tk_master=None, *args, **kwargs):
        tk_master = tk_master if tk_master else master
        Frame.__init__(self, tk_master, bd=1, relief='raised', *args, **kwargs)

        Label(self, text=text, bd=1, relief='sunken').pack(side='top', padx=5,
                                                           pady=5)

        self.master = master
        self.choice_var = StringVar()
        self.radio_group = []

        self.choice_var.trace('w', self.master.update_all)

    def generate_contents(self, contents):
        """
        :param contents: Contents to generate as tk radios
        """
        for item in contents:
            radio = Radiobutton(self, text=item, variable=self.choice_var, value=item)
            radio.pack(side='top')
            self.radio_group.append(radio)

    def update_available(self, type, event=None):
        for radio in self.radio_group:
            if radio['value'] in type:
                if radio['value'] != self.choice_var.get():
                    radio.config(state='disabled')
            else:
                radio.config(state='active')


class RotorSlot(BaseSlot):
    def __init__(self, master, index, tk_master=None, *args, **kwargs):
        text = ('SLOW', 'MEDIUM', 'FAST')[index] + ' ROTOR'
        BaseSlot.__init__(self, master, text, tk_master, *args, **kwargs)

        self.index = index

        self.generate_contents(DataStorage.get_info('Enigma1', 'rotor'))

        # Ring setting indicator
        setting_idx = self.master.enigma.ring_settings[index]

        self.ring_var = StringVar(value=labels[setting_idx])

        Label(self, text='RING\nSETTING', bd=1, relief='sunken').pack(
            side='top', fill='x', padx=4)
        OptionMenu(self, self.ring_var, *labels).pack(side='top')

        self.choice_var.set(self.master.enigma.rotors[index].label)
        self.ring_var.trace('w', self.master.update_all)

    def update_selected(self, event=None):
        self.master.curr_rotors[self.index] = self.choice_var.get()
        ring_setting = labels.index(self.ring_var.get())
        self.master.curr_ring_settings[self.index] = ring_setting

    def update_available(self, *event):
        BaseSlot.update_available(self, type=self.master.curr_rotors)


class ReflectorSlot(BaseSlot):
    def __init__(self, master, tk_master=None, *args, **kwargs):
        BaseSlot.__init__(self, master, 'REFLECTOR', tk_master, *args, **kwargs)

        self.generate_contents(DataStorage.get_info('Enigma1', 'reflector'))
        self.choice_var.set(self.master.enigma.reflector.label)

    def update_selected(self, *event):
        self.master.curr_reflector = self.choice_var.get()

    def update_available(self, *event):
        BaseSlot.update_available(self, type=[self.master.curr_reflector])
