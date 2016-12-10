from tkinter import Frame, StringVar, Label, Entry
from re import sub


class PlugSocket(Frame):
    """Custom made socket class"""

    def __init__(self, parent, label, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self._label = label

        input_trace = StringVar()
        input_trace.set('')

        Label(self, text=label).pack(side='top')

        self.plug_socket = Entry(self, width=2, justify='center',
                                 textvariable=input_trace)

        input_trace.trace('w', self.update_entry)

        self.plug_socket.pack(side='bottom', pady=5)

    @property
    def label(self):
        return self._label[0]

    @property
    def socket(self):
        """Gets string value of the socket"""
        return [self.label, self.plug_socket.get()]

    def update_entry(self, *args, character=''):
        """Ensures only a single, uppercase letter is entered"""
        socket_data = self.socket[1]  # Data from the entry
        raw = character[0].upper() if character else self.socket[1][0].upper()
        self.plug_socket.delete('0', 'end')
        if raw:
            pattern = r"[^A-Za-z]|[%s]" % self.label
            string = sub(pattern, '', raw.upper())[0]
            if string and string not in used_letters:
                self.plug_socket.insert('0', string)

    def clear(self):
        self.plug_socket.delete('0', 'end')
