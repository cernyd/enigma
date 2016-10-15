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

    def rotate_first(self):
        index = 0
        rot_next = False
        for _ in self.__rotor_pos:
            if index == 0:
                if self.__rotor_pos[index] == 25:
                    self.__rotor_pos[index] = 0
                    rot_next = True
                else:
                    self.__rotor_pos[index] += 1
            elif rot_next:
                if self.__rotor_pos[index] == 25:
                    self.__rotor_pos[index] = 0
                    rot_next = True
                else:
                    self.__rotor_pos[index] += 1
                    rot_next = False
            index += 1

    def final_letter(self, letter, offset):
        final_index = alphabet.index(letter) + offset

        if final_index > len(alphabet) - 1:
            return alphabet[final_index - len(alphabet)]
        else:
            return alphabet[final_index]

    def button_press(self, button):
        output_letter = self.etw.route_signal(button)  # Correct function

        index = 0
        for rotor in self.rotors:
            """
            output_letter = self.final_letter(output_letter,
                                              self.__rotor_pos[index])
            """
            output_letter = rotor.route_signal(output_letter)
            index += 1

        output_letter = self.ukw.route_signal(output_letter)  # Works correctly

        index = -2
        for rotor in reversed(self.rotors):
            """
            output_letter = self.final_letter(output_letter,
                                              self.__rotor_pos[index])
            """
            output_letter = rotor.route_signal(output_letter, 'back')
            index += 1

        output_letter = self.etw.route_signal(output_letter, 'back')  # Correct function

        self.rotate_first()
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
for letter in 'OXKN':
    output += enigma.button_press(letter)

print(output)
