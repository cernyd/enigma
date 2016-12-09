from tkinter import Toplevel, Frame, Button
from misc import get_icon
from slot import Slot


class RotorMenu(Toplevel):
    """GUI for setting rotor order, reflectors and ring settings"""
    def __init__(self, enigma_instance, *args, **kwargs):
        Toplevel.__init__(self, bg='gray85', *args, **kwargs)

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^
        self.enigma = enigma_instance
        self.curr_rotors = ['', '', '']
        self.curr_reflector = ''
        self.curr_ring_settings = [0, 0, 0]

        # Window config
        self.grab_set()
        self.iconbitmap(get_icon('rotor.ico'))
        self.resizable(False, False)
        self.wm_title("Rotor order")

        # Frames
        main_frame = Frame(self)
        main_frame.config(bg='red')
        button_frame = Frame(self)
        button_frame.config(bg='gray85')

        # Buttons

        self.apply_button = Button(button_frame, text='Apply', width=12,
                                   command=self.apply)

        self.apply_button.pack(side='right', padx=5, pady=5)

        self.storno_button = Button(button_frame, text='Storno', width=12,
                                    command=self.storno)

        self.storno_button.pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

        # Creating slots...
        self.reflector = Slot(main_frame, self, self.enigma, kind='reflector')

        self.rotors = []
        [self.rotors.append(Slot(main_frame, self, self.enigma, index=index)) for index in range(3)]

        # Packing...
        self.reflector.pack(side='left', fill='y', padx=(10, 2), pady=5)
        [rotor.pack(side='left', padx=2, pady=5, fill='y') for rotor in self.rotors]

        main_frame.pack(side='top', pady=(5, 0), padx=(8,0))

    def storno(self):
        """Resets all values and destroys the window"""
        self.rotor_vars = []
        self.ring_setting_vars = []
        self.destroy()

    def apply(self):
        self.enigma.rotors = self.curr_rotors
        self.enigma.reflector = self.curr_reflector
        self.enigma.ring_settings = self.curr_ring_settings
        self.destroy()

    def can_apply(self, event=None):
        """Sets the apply button to active or disabled based on criteria"""
        pass


