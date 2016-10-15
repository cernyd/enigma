from rotor import Enigma1


class Enigma:
    def __init__(self, rotor_order, plugboard_settings=None):
        self.__rotor_order = rotor_order
        self.__plugboard_settings = plugboard_settings
        print(self.__rotor_order)

    def button_press(self, button):
        input_letter = button

        return input_letter

    def plugboard(self):
        pass


my_enigma = Enigma([rotor for rotor in Enigma1.rotors.values()])
