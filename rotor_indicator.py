from tkinter import Frame, Label, Button


def format_digit(number: int) -> str:
    """Adds returns 01 when 1 entered etc."""
    number = str(number)
    if len(number) != 2:
        number = '0' + number
    return number


class RotorIndicator(Frame):
    """Rotor indicator for indicating or rotating a rotor"""
    def __init__(self, master, enigma_instance, playback_instance, index):
        """
        :param master: Master for tkinter
        :param enigma_instance: Global enigma instance
        :param playback_instance: Sound playback instance
        :param index: Indicator index to show correct values
        """
        Frame.__init__(self, master, bg='gray85')
        self.index = index

        cfg = dict(font=('Arial', 10), width=1)

        Button(self, text='+', command=lambda: self.rotate(1), **cfg).pack(
            side='top')

        self.indicator = Label(self, bd=1, relief='sunken', width=2)

        Button(self, text='-', command=lambda: self.rotate(-1), **cfg).pack(
            side='bottom')

        self.indicator.pack(side='top', pady=10, padx=20)

        self.playback = playback_instance
        self.enigma = enigma_instance
        self.update_indicator()

    def rotate(self, places=0):
        """
        Rotates the rotor with the selected index backward
        :param places: How many places to rotate ( negative = backwards )
        """
        self.playback.play('click')
        self.enigma.rotors[self.index].rotate(places)
        self.update_indicator()

    def update_indicator(self, event=None):
        raw = self.enigma.rotors[self.index].position_ring[0]
        self.indicator.config(text=format_digit(raw))
