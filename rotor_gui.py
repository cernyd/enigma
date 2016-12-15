from tkinter import Toplevel, Frame, Button
from misc import get_icon, baseinit
from slot import ReflectorSlot, RotorSlot


class RotorMenu(Toplevel):
    """GUI for setting rotor order, reflectors and ring settings"""
    def __init__(self, enigma_instance, *args, **kwargs):
        """
        :param enigma_instance: Global enigma instance
        """
        # Superclass constructor call
        Toplevel.__init__(self, bg='gray85', *args, **kwargs)

        baseinit(self)

        # Window config
        self.iconbitmap(get_icon('rotor.ico'))
        self.wm_title("Rotor order")

        # Enigma settings buffer
        self.enigma = enigma_instance
        self.curr_rotors = [rotor.label for rotor in self.enigma.rotors]
        self.curr_reflector = self.enigma.reflector.label
        self.curr_ring_settings = self.enigma.ring_settings

        # Frames
        main_frame = Frame(self, bg='gray85')
        button_frame = Frame(self, bg='gray85')

        # Buttons
        Button(button_frame, text='Apply', width=12, command=self.apply).pack(
            side='right', padx=5, pady=5)


        Button(button_frame, text='Storno', width=12,
               command=self.destroy).pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

        # Slots for settings
        self.reflector = ReflectorSlot(self, main_frame)
        self.reflector.pack(side='left', fill='y', padx=(10, 2), pady=5)

        self.rotors = [RotorSlot(self, index, main_frame) for index in range(3)]
        [rotor.pack(side='left', padx=2, pady=5, fill='y') for rotor in self.rotors]

        main_frame.pack(side='top', pady=(5, 0), padx=(0,10))

        self.update_all()

    def apply(self):
        """Applies all settings to the global enigma instance"""
        self.enigma.rotors = self.curr_rotors
        self.enigma.reflector = self.curr_reflector
        self.enigma.ring_settings = self.curr_ring_settings
        self.destroy()

    def update_all(self, *event):
        """Updates available radios for all slots"""
        try:
            for rotor in self.rotors:
                rotor.update_selected()
            for rotor in self.rotors:
                rotor.update_available()
        except AttributeError: # If the rotor group does not exist yet
            pass
