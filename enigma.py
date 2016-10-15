from rotor import Enigma1


alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Enigma:
    def __init__(self, etw, rotors, ukw, starting_pos=[0, 0, 0], plugboard_settings=None):
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
        self.set_rotor_pos(starting_pos)


    def set_rotor_pos(self, pos_list):
        self.__rotor_pos = pos_list

    def button_press(self, button):
        output_letter = self.etw.route_signal(button)  # Correct function

        for rotor in self.rotors:
            output_letter = rotor.route_signal(output_letter)

        output_letter = self.ukw.route_signal(output_letter)  # Works correctly

        for rotor in reversed(self.rotors):
            output_letter = rotor.route_signal(output_letter, 'back')

        output_letter = self.etw.route_signal(output_letter, 'back')  # Correct function

        return output_letter

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


output = ''
for letter in 'NBSISINBCSTNCTLCLAJNFJN':
    output += enigma.button_press(letter)

print(output)
