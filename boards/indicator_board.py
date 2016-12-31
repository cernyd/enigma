from tkinter import Frame, Label, Button

from misc import font, bg


class IndicatorBoard(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.enigma = self.master.enigma

        self.indicators = []
        for index in range(3):
            indicator = RotorIndicator(self, index)
            self.indicators.append(indicator)
            indicator.pack(side='left')

    def update_indicators(self):
        [indicator.update_indicator() for indicator in self.indicators]


def format_digit(number: int) -> str:
    """Adds returns 01 when 1 entered etc."""
    number = str(number)
    if len(number) != 2:
        number = '0' + number
    return number


class RotorIndicator(Frame):
    """Rotor indicator for indicating or rotating a rotor"""

    def __init__(self, master, index):
        Frame.__init__(self, self, bg=bg)
        self.index = index

        self.enigma = master.enigma

        cfg = dict(font=font, width=1)

        Button(self, text='+', command=lambda: self.rotate(1), **cfg).pack(
            side='top')

        self.indicator = Label(self, bd=1, relief='sunken', width=2)

        Button(self, text='-', command=lambda: self.rotate(-1), **cfg).pack(
            side='bottom')

        self.indicator.pack(side='top', pady=10, padx=20)

        self.enigma = enigma_instance
        self.update_indicator()

    def rotate(self, places=0):
        """
        Rotates the rotor with the selected index backward
        :param places: How many places to rotate ( negative = backwards )
        """
        self.master.master.playback.play('click')
        self.enigma.rotors[self.index].rotate(places)
        self.update_indicator()

    def update_indicator(self, event=None):
        raw = self.enigma.rotors[self.index].position_ring[0]
        self.indicator.config(text=raw)
