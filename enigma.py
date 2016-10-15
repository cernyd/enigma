from rotor import Enigma1


class Enigma:
    def __init__(self, etw, rotors, ukw, plugboard_settings=None):
        self.ukw = ukw
        self.etw = etw
        self.rotors = rotors
        self.plugboard_settings = plugboard_settings

    def button_press(self, button):
        input_letter = button

        return input_letter

    def plugboard(self):
        pass


my_enigma = Enigma()
