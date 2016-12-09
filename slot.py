from tkinter import Frame, Label, StringVar, Radiobutton, OptionMenu
from misc import Enigma1

ring_labels = Enigma1.labels

class Slot(Frame):
    def __init__(self, master, enigma_instance, index=0, kind='rotor', *args, **kwargs):
        Frame.__init__(self, master, bd=1, relief='raised', *args, **kwargs)

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

        self.choice_var.trace('w', self.update_selected)

        items = []
        if kind == 'rotor':
            items.extend(list(Enigma1.rotors.keys()))
            self.generate_contents(items)
            self.socket_idx += 1

            # Ring setting indicator
            self.ring_var = StringVar()
            setting_idx = self.enigma.rotors[index].ring_setting
            curr_setting = ring_labels[setting_idx]

            self.ring_var.set(curr_setting)

            Label(self, text='RING\nSETTING', bd=1, relief='sunken').pack(side='top', fill='x', padx=4)

            OptionMenu(self, self.ring_var, *ring_labels).pack(side='top')
            self.ring_var.trace('w', self.update_selected)
            self.choice_var.set(self.enigma.rotors[index].get_label())

        elif kind == 'reflector':
            items.extend(list(Enigma1.reflectors.keys()))
            self.generate_contents(items)

            self.choice_var.set(self.enigma.reflector.get_label())

    def generate_contents(self, contents):
        for item in contents:
            radio = Radiobutton(self, text=item, variable=self.choice_var, value=item)
            radio.pack(side='top')
            self.radio_group.append(radio)

    def update_selected(self, *event):
        print(event)
        print('HERE')
        # if self.kind == 'reflector':
        #     self.master.curr_selected[self.index] = self.choice_var.get()
        # elif self.kind == 'rotor':
        #     self.master.curr_selected[self.index+1] = self.choice_var.get()
        #     self.master.curr_ring_settings[self.index] = self.ring_var.get()

    def get_info(self):
        if self.kind == 'rotor':
            return [self.choice_var.get(), self.ring_var.get()]
        else:
            return [self.choice_var.get()]
