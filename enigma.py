from rotor import Enigma1


class Enigma:
    def __init__(self, etw, rotors, ukw, plugboard_settings=None):
        """
        UKW - Reflector
        ETW - Stationary router
        """

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

    def __str__(self):
        rotor_settings = ["Rotor: %s | Offset: %s" %
                          (rotor.rotor_label, rotor.rotor_offset)
                          for rotor in self.rotors]
        ukw = "UKW: %s" % (self.ukw.rotor_label)
        etw = "ETW: %s" % (self.etw.rotor_label)
        return "- Enigma -\n{}\n{}\n{}".format(ukw, '\n'.join(rotor_settings), etw)


rotors = Enigma1.rotors
enigma = Enigma(rotors['ETW'], [rotors['I'],
                                rotors['II'],
                                rotors['III']],
                                rotors['UKW-A'])
print(enigma)
