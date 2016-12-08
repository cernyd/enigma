from tkinter import Toplevel, Frame, Radiobutton, Label, StringVar, Button, OptionMenu
from misc import Enigma1, get_icon


ring_labels = Enigma1.labels


class RotorMenu(Toplevel):
    """GUI for setting rotor order, reflectors and ring settings"""
    def __init__(self, enigma_instance, *args, **kwargs):
        Toplevel.__init__(self, bg='gray85', *args, **kwargs)

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        self.enigma = enigma_instance
        self.curr_rotors = ['','','','']
        self.curr_ring_settings = [0,0,0]

        # Window config
        self.grab_set()
        self.iconbitmap(get_icon('rotor.ico'))
        self.resizable(False, False)
        self.wm_title("Rotor order")

        # Frames
        main_frame = Frame(self)
        main_frame.config(bg='gray85')
        button_frame = Frame(self)
        button_frame.config(bg='gray85')

        # Buttons

        self.apply_button = Button(button_frame, text='Apply',
                                   command=self.destroy,
                                   width=12)

        self.apply_button.pack(side='right', padx=5, pady=5)

        self.storno_button = Button(button_frame, text='Storno',
                                    command=self.storno,
                                    width=12)

        self.storno_button.pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

        # Creating slots...
        self.reflector = Slot(main_frame, self.enigma, kind='reflector')

        self.rotors = []
        [self.rotors.append(Slot(main_frame, self.enigma, index=index)) for index in range(3)]

        # Packing...
        self.reflector.pack(side='left', fill='y', padx=2, pady=5)
        [rotor.pack(side='left', padx=2, pady=5, fill='y') for rotor in self.rotors]

        main_frame.pack(side='top', pady=(5, 0), padx=10)

    def storno(self):
        """Resets all values and destroys the window"""
        self.rotor_vars = []
        self.ring_setting_vars = []
        self.destroy()

    def can_apply(self, event=None):
        """Sets the apply button to active or disabled based on criteria"""
        pass


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
            self.choice_var.set(self.enigma.rotors[index].get_label())
            self.ring_var.trace('w', self.update_selected)

        elif kind == 'reflector':
            items.extend(list(Enigma1.reflectors.keys()))
            self.generate_contents(items)
            self.choice_var.set(self.enigma.reflector.get_label())
        self.choice_var.trace('w', self.update_selected)

    def generate_contents(self, contents):
        for item in contents:
            radio = Radiobutton(self, text=item, variable=self.choice_var, value=item)
            radio.pack(side='top')
            self.radio_group.append(radio)

    def update_selected(self, event=None):
        if self.kind == 'reflector':
            self.master.curr_selected[self.index] = self.choice_var.get()
        elif self.kind == 'rotor':
            self.master.curr_selected[self.index+1] = self.choice_var.get()
            self.master.curr_ring_settings[self.index] = self.ring_var.get()
        print(self.master.curr_selected)

    def write_changes(self):
        pass

    def get_info(self):
        if self.kind == 'rotor':
            return [self.choice_var.get(), self.ring_var.get()]
        else:
            return [self.choice_var.get()]
