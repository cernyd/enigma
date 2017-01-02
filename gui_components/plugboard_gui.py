from re import sub
from tkinter import Frame, Label, Entry, StringVar, Button, Toplevel

from enigma_components.rotor_factory import data_interface
from misc import get_icon, baseinit


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

        for row in data_interface('layout'):
            new_row = Frame(self)
            for item in row:
                self.plug_sockets.append(PlugSocket(new_row, self,
                                                    data_interface('labels')[
                                                        item]))
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

        my_pair = [pair for pair in self.master.enigma.plugboard if
                   self.label in pair]

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


class PlugEntry(Entry):
    def __init__(self, tk_master, master, *args, **kwargs):
        # Superclass constructor call
        internal_tracer = StringVar()

        Entry.__init__(self, tk_master, *args, **kwargs,
                       textvariable=internal_tracer)

        internal_tracer.trace('w', self.event)

        self.master = master
        self.last_val = ''

    def event(self,
              *event):  # Needs some refactoring ( unreliable and confusing )
        new_val = self.validate(self.get())  # Raw new data
        delete = self.last_val and not new_val
        write = not self.last_val and new_val

        self.set(new_val)
        self.last_val = new_val

        if delete:
            self.master.callback('DELETE')
        elif write:
            self.master.callback('WRITE')

    def clear(self):
        self.delete('0', 'end')

    def set(self, string):
        self.clear()
        self.insert(0, string)

    def get(self):
        return Entry.get(self).upper()

    def validate(self, raw):
        forbidden = ''.join(self.master.local_forbidden)
        raw = sub('([\s]|[%s])+' % forbidden, '', raw).upper()
        return raw[0] if raw else raw
