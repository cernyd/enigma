from tkinter import Frame, Label
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

        # Loading data

        my_pair = [pair for pair in self.master.enigma.plugboard if self.label in pair]

        if my_pair:
            my_pair = my_pair[0]
            if my_pair[0] != self.label:
                self.plug_socket.set(my_pair[0])
            else:
                self.plug_socket.set(my_pair[1])

    def link(self, target='', obj=None):  # This whole class is a mess
        if not obj:  # Link constructed locally
            if target:
                obj = self.master.get_target(target)
                if obj:
                    obj.link(obj=self)
                else:
                    return
            else:
                print('Invalid (empty) link call.')
                return
        self.plug_socket.set(obj.label)
        self.pair = obj
        self.master.add_used(self.label)

    def unlink(self, external=False):  # Attempting to unlink after each delete!
        self.master.delete_used(self.label)
        if self.pair:
            if not external:  # Would cause a loop presumably
                self.pair.unlink(True)
            self.plug_socket.clear()
            self.pair = None
        else:
            print('Invalid unlink attempt (object not linked).')

    @property
    def label(self):
        return self._label[0]

    def get_socket(self):
        return self.plug_socket.get()

    @property
    def local_forbidden(self):
        if self.label not in self.master.used:
            return [self.label] + self.master.used
        else:
            return self.master.used

    def callback(self, event_type):
        """Callback from the plug_entry widget"""
        print('Event > ', event_type)
        if event_type == 'WRITE':
            self.link(self.plug_socket.get())
        elif event_type == 'DELETE':
            self.unlink()
