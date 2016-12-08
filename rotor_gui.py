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

        # Bindings
        self.bind('<Button-1>', self.checkup)

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
        self.reflector = Slot(main_frame, self.enigma, type='reflector')

        self.rotors = []
        [self.rotors.append(Slot(main_frame, self.enigma, index=index)) for index in range(3)]

        # Packing...
        self.reflector.pack(side='left', fill='y', padx=2, pady=5)
        [rotor.pack(side='left', padx=2, pady=5, fill='y') for rotor in self.rotors]

        main_frame.pack(side='top', pady=(5, 0), padx=10)

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


class Slot(Frame):
    def __init__(self, master, enigma_instance, index=0, type='rotor', *args, **kwargs):
        Frame.__init__(self, master, bd=1, relief='raised', *args, **kwargs)

        labels = ('THIRD', 'SECOND', 'FIRST')

        text = ''

        if type == 'rotor':
            text = labels[index] + ' ROTOR'
        elif type == 'reflector':
            text = 'REFLECTOR'

        Label(self, text=text, bd=1, relief='sunken').pack(side='top', padx=5, pady=5)

        self.enigma = enigma_instance

        self.choice_var = StringVar()

        self.radio_group = []

        items = []
        if type == 'rotor':
            items.extend(list(Enigma1.rotors.keys()))
            self.generate_contents(items)

            # Ring setting indicator
            self.ring_var = StringVar()
            setting_idx = self.enigma.rotors[index].ring_setting
            curr_setting = ring_labels[setting_idx]

            self.ring_var.set(curr_setting)

            Label(self, text='RING\nSETTING', bd=1, relief='sunken').pack(side='top', fill='x', padx=4)

            OptionMenu(self, self.ring_var, *ring_labels).pack(side='top')
            self.choice_var.set(self.enigma.rotors[index].get_label())

        elif type == 'reflector':
            items.extend(list(Enigma1.reflectors.keys()))
            self.generate_contents(items)
            self.choice_var.set(self.enigma.reflector.get_label())

    def generate_contents(self, contents):
        for item in contents:
            radio = Radiobutton(self, text=item, variable=self.choice_var, value=item)
            radio.pack(side='top')
            self.radio_group.append(radio)
