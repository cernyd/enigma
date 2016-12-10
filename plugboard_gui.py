from tkinter import Toplevel, Entry, Label, Frame, StringVar, Button
from misc import get_icon, Enigma1, unique_pairs
from plug_socket import PlugSocket

layout = [[16, 22, 4, 17, 19, 25, 20, 8, 14],  # Plugboard is layed out like a keyboard
          [0, 18, 3, 5, 6, 7, 9, 10],
          [15, 24, 23, 2, 21, 1, 13, 12, 11]]


labels = Enigma1.labels
used_letters = []


class PlugboardMenu(Toplevel):
    """GUI for visual plugboard pairing setup"""
    def __init__(self, enigma_instance, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.enigma = enigma_instance
        self.used_letters = []

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # self.bind('<Key>', self.update_pairs)

        # Window config
        self.grab_set()
        self.iconbitmap(get_icon('plugboard.ico'))
        # self.resizable(False, False)
        self.wm_title("Plugboard")

        rows = []
        self.plug_sockets = []

        for row in layout:
            new_row = Frame(self)
            for item in row:
                self.plug_sockets.append(PlugSocket(new_row, labels[item]))
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
        # self.enigma = unique_pairs(self.get_pairs())
        self.destroy()
