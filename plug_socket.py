from tkinter import Frame, StringVar, Label
from plug_entry import PlugEntry


class PlugSocket(Frame):
    """Custom made socket class"""

    def __init__(self, tk_master, master, label, *args, **kwargs):
        Frame.__init__(self, tk_master, *args, **kwargs)

        self._label = label
        self.master = master
        self.pair = None

        Label(self, text=label).pack(side='top')

        self.plug_socket = PlugEntry(self, self, width=2, justify='center')

        self.plug_socket.pack(side='bottom', pady=5)

        my_pair = [pair for pair in self.master.enigma.plugboard if self.label in pair]

        if my_pair:
            my_pair = my_pair[0]
            if my_pair[0] != self.label:
                self.plug_socket.set(my_pair[0])
            else:
                self.plug_socket.set(my_pair[1])

    def link(self, target='', obj=None):
        self.master.add_used(self.label)
        if not obj:  # Link constructed locally
            if target:
                obj = self.master.get_target(target)
                obj.link(obj=self)
                self.master.add_pair([self.label, obj.label])
            else:
                print('Invalid (empty) link call.')
        self.plug_socket.set(obj.label)
        self.pair = obj

    def unlink(self, external=False):
        self.master.delete_used(self.label)
        if self.pair:
            if not external: # Would cause a loop presumably
                self.pair.unlink(True)
            self.master.remove_pair([self.label, self.pair.label])
            self.plug_socket.clear()
            self.pair = None
        else:
            print('Invalid unlink attempt (object not linked).')

    @property
    def label(self):
        return self._label[0]

    @property
    def local_forbidden(self):
        if self.label not in self.master.used:
            return [self.label] + self.master.used
        else:
            return self.master.used

    def callback(self, event_type):
        """Callback from the plug_entry widget"""
        if event_type == 'WRITE':
            self.link(self.plug_socket.get())
        elif event_type == 'DELETE':
            self.unlink()
