from tkinter import Frame, Label
from misc import Enigma1


class Lightboard(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, bd=1, relief='raised', bg='gray85', *args, *kwargs)

        rows = []
        self.bulbs = []

        for row in Enigma1.layout:
            new_row = Frame(self)
            for item in row:
                text = Enigma1.labels[item][0]
                self.bulbs.append(
                    Label(new_row, text=text, font=('Arial', 14), bg='gray85',
                          padx=2))
            rows.append(new_row)

        for row in rows:
            row.pack(side='top')

        for item in self.bulbs:
            item.pack(side='left')

        self.last_bulb = None

    def light_up(self, letter=''):
        if self.last_bulb:
            self.last_bulb.config(fg='black')
        if letter:
            for bulb in self.bulbs:
                if bulb['text'] == letter:
                    bulb.config(fg='yellow')
                    self.last_bulb = bulb
                    break
