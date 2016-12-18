from tkinter import Toplevel, Frame, Button
from misc import get_icon, baseinit
from plug_socket import PlugSocket


class PlugboardMenu(Toplevel):
    """GUI for visual plugboard pairing setup"""
    def __init__(self, enigma_instance, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        baseinit(self)

        self.enigma = enigma_instance
        self.used = []  # All used letters
        self._pairs = self.enigma.plugboard  # Pairs to return

        # Window config
        self.iconbitmap(get_icon('plugboard.ico'))
        self.wm_title("Plugboard")

        rows = []
        self.plug_sockets = []

        for row in layout:
            new_row = Frame(self)
            for item in row:
                self.plug_sockets.append(PlugSocket(new_row, self, labels[item]))
            rows.append(new_row)

        for row in rows:
            row.pack(side='top')

        for item in self.plug_sockets:
            item.pack(side='left')

        button_frame = Frame(self)

        self.apply_button = Button(button_frame, text='Apply',
                                   command=self.apply,
                                   width=12)

        self.storno_button = Button(button_frame, text='Storno',
                                    command=self.destroy,
                                    width=12)

        self.apply_button.pack(side='right', padx=5, pady=5)
        self.storno_button.pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

    def apply(self):
        self.enigma.plugboard = self.pairs
        self.destroy()

    def delete_used(self, letter):
        try:
            self.used.remove(letter)
        except ValueError:
            pass

    def add_used(self, letter):
        if letter not in self.used:
            self.used.append(letter)

    def get_target(self, label):
        for socket in self.plug_sockets:
            if socket.label == label:
                return socket

    @property
    def pairs(self):
        pairs = []
        for socket in self.plug_sockets:
            pair = [socket.label, socket.get_socket()]
            if all(pair) and pair not in pairs and list(reversed(pair)) not in pairs:
                pairs.append(pair)
        return pairs
