from tkinter import Toplevel, Frame, Button
from misc import get_icon
from slot import ReflectorSlot, RotorSlot


class RotorMenu(Toplevel):
    """GUI for setting rotor order, reflectors and ring settings"""
    def __init__(self, enigma_instance, *args, **kwargs):
        """
        :param enigma_instance: Global enigma instance
        """
        # Superclass constructor call
        Toplevel.__init__(self, bg='gray85', *args, **kwargs)

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Window config
        self.grab_set()
        self.iconbitmap(get_icon('rotor.ico'))
        self.resizable(False, False)
        self.wm_title("Rotor order")

        # Enigma settings buffer
        self.enigma = enigma_instance
        self.curr_rotors = ['', '', '']
        self.curr_reflector = ''
        self.curr_ring_settings = [0, 0, 0]

        # Frames
        main_frame = Frame(self, bg='gray85')
        button_frame = Frame(self, bg='gray85')

        # Buttons
        apply_button = Button(button_frame, text='Apply', width=12,
                                   command=self.apply)

        apply_button.pack(side='right', padx=5, pady=5)

        storno_button = Button(button_frame, text='Storno', width=12,
                                    command=self.destroy)

        storno_button.pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

        # Slots for settings
        self.reflector = ReflectorSlot(main_frame, self, self.enigma, kind='reflector')

        self.rotors = []
        [self.rotors.append(RotorSlot(main_frame, self, index=index)) for index in range(3)]

        self.reflector.pack(side='left', fill='y', padx=(10, 2), pady=5)
        [rotor.pack(side='left', padx=2, pady=5, fill='y') for rotor in self.rotors]

        main_frame.pack(side='top', pady=(5, 0), padx=(0,10))

        self.update_all()

    def apply(self):
        """Applies all settings to the global enigma instance"""
        self.enigma.rotors = self.curr_rotors
        self.enigma.reflector = self.curr_reflector
        self.enigma.ring_settings = self.curr_ring_settings
        self.destroy()

    def update_all(self):
        """Updates available radios for all slots"""
        try:
            for rotor in self.rotors:
                rotor.update_available()
        except AttributeError: # If the rotor group does not exist yet
            pass
