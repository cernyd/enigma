from rotor import Enigma1, Rotor


class Enigma:
    def __init__(self, etw, rotors, ukw, plugboard_settings=None):

        if len(rotors) < 3:
            raise AssertionError('Not enough rotors!')
        elif len(rotors) > 3:
            raise AssertionError('Too many rotors!')
        else:
            self.rotors = rotors

        if not ukw:
            raise AssertionError('No reflector!')
        else:
            self.ukw = ukw

        if not etw:
            raise AssertionError('No entry wheel!')
        else:
            self.etw = etw

        self.plugboard_settings = plugboard_settings

    def button_press(self, button):
        input_letter = button

        return input_letter

    def plugboard(self):
        pass


rotor_test = Rotor('I', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1)
