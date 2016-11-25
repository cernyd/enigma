from tkinter import Toplevel, Entry, Label, Frame, StringVar, Button
from misc import get_icon, Enigma1
from re import sub


layout = [[16,22,4,17,19,25,20,8,14],
          [0,18,3,5,6,7,9,10],
          [15,24,23,2,21,1,13,12,11]]


labels = Enigma1.labels


class PlugboardMenu(Toplevel):
    """GUI for visual plugboard pairing setup"""

    return_data = None

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        self.bind('<Key>', self.update_pairs)

        # Window config
        self.grab_set()
        self.iconbitmap(get_icon('plugboard.ico'))
        #self.resizable(False, False)
        self.wm_title("Plugboard")

        self.rows = []
        self.plug_sockets = []

        for row in layout:
            new_row = Frame(self)
            for item in row:
                self.plug_sockets.append(PlugSocket(new_row, labels[item]))
            self.rows.append(new_row)

        for row in self.rows:
            row.pack(side='top')

        for item in self.plug_sockets:
            item.pack(side='left')

        button_frame = Frame(self)

        self.apply_button = Button(button_frame, text='Apply',
                                   command=self.safe_destroy,
                                   width=12)

        self.storno_button = Button(button_frame, text='Storno',
                                    command=self.storno,
                                    width=12)

        self.apply_button.pack(side='right', padx=5, pady=5)
        self.storno_button.pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

    def update_pairs(self, event=None):
        used = []
        index = 0
        for pair in self.get_pairs():
            index += 1

    def get_pairs(self):
        return [socket.get_socket() for socket in self.plug_sockets]

    def safe_destroy(self):
        PlugboardMenu.return_data = self.get_pairs()
        self.destroy()

    def storno(self):
        self.plug_sockets = []
        self.destroy()


class PlugSocket(Frame):
    """Custom made socket class"""
    def __init__(self, parent, label, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.label = label

        input_trace = StringVar()
        input_trace.set('')

        Label(self, text=label).pack(side='top')

        self.plug_socket = Entry(self, width=2, justify='center', textvariable=input_trace)

        input_trace.trace('w', self.update_socket)

        self.plug_socket.pack(side='bottom', pady=5)

    def get_socket(self):
        """Gets string value of the socket"""
        return self.label[0], self.plug_socket.get()

    def update_socket(self, *args, character=''):
        """Ensures only a single, uppercase letter is entered"""
        raw = character if character else self.plug_socket.get()
        self.plug_socket.delete('0', 'end')
        if raw:
            string = sub(r"[^A-Za-z]|[%s]" % (self.label[0]), '', raw.upper())[0].upper()
            if string:
                self.plug_socket.insert('0', string)

    def clear(self):
        self.plug_socket.delete('0', 'end')
