from tkinter import Entry, StringVar
from re import sub


class PlugEntry(Entry):
    def __init__(self, tk_master, master, *args, **kwargs):
        # Superclass constructor call
        internal_tracer = StringVar()

        Entry.__init__(self, tk_master, *args, **kwargs,
                       textvariable=internal_tracer)

        internal_tracer.trace('w', self.event)

        self.master = master

        self.last_val = ''

    def event(self, *event):
        new_val = self.validate(self.get()) # Raw new data
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
        raw = sub('([\s]|[%s])+' % (forbidden), '', raw).upper()
        return raw[0] if raw else raw
