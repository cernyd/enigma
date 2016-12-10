from tkinter import Frame, StringVar, Label
from plug_entry import PlugEntry


class PlugSocket(Frame):
    """Custom made socket class"""

    def __init__(self, parent, label, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self._label = label

        Label(self, text=label).pack(side='top')

        self.plug_socket = PlugEntry(self, self, width=2, justify='center')

        self.plug_socket.pack(side='bottom', pady=5)

    def link(self):
        pass

    def unlink(self):
        pass

    def event(self):
        print('PLUG EVENT')