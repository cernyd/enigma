from tkinter import Entry, StringVar
from re import sub


class PlugEntry(Entry):
    def __init__(self, tk_master, master, *args, **kwargs):
        # Superclass constructor call
        internal_tracer = StringVar()

        Entry.__init__(self, tk_master, *args, **kwargs,
                       textvariable = internal_tracer)

        internal_tracer.trace('w', self.change)

        self.master = master

        self.last_val = ''

    def change(self, *event):
        new_val = self.validate(self.get()) # Raw new data

        delete = self.last_val and not new_val
        write = not self.last_val and new_val

        if delete or write: # Event type detection
            if delete:
                print('DELETED')
            elif write:
                print('WRITTEN')
        else:
            print('NO CHANGE')

        self.set(new_val)
        self.last_val = new_val

    def clear(self):
        self.delete('0', 'end')

    def set(self, string):
        self.clear()
        self.insert(0, string)

    def get(self):
        return Entry.get(self).upper()

    def validate(self, raw):
        raw = sub('([\s]|[A])+', '', raw).upper()

        if raw:
            raw = raw[0]

        return raw
