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
        self.__rotor_pos = starting_pos

    def set_rotor_pos(self, pos_list):
        self.__rotor_pos = pos_list

    def rotate_first(self):
        index = 0
        rot_next = False

        for _ in self.__rotor_pos:
            if index == 0 or rot_next:
                if self.__rotor_pos[index] == 26:
                    self.__rotor_pos[index] = 0
                    rot_next = True
                else:
                    self.__rotor_pos[index] += 1
                    if index != 0:
                        rot_next = False
            index += 1

    def correct_position(self, letter, rotor_idx, side='front'):


        if side == 'front':
            alphabet = self.rotors[rotor_idx].front_alphabet
        elif side == 'back':
            alphabet = self.rotors[rotor_idx].back_alphabet
        print(side, ' > ', alphabet)
        final_idx = alphabet.index(letter) + self.__rotor_pos[rotor_idx]

        if final_idx >= len(alphabet):
            return alphabet[final_idx - len(alphabet)]
        else:
            return alphabet[final_idx]

    def button_press(self, button):
        output_letter = self.etw.route_signal(button)  # Correct function

        self.rotate_first()  # Rotor rotates first, THEN encrypts

        rotor_idx = 0
        for rotor in self.rotors:
            print('Before correction > ', output_letter)
            output_letter = self.correct_position(output_letter, rotor_idx)
            print('After correction > ', output_letter)
            output_letter = rotor.route_signal(output_letter)

            rotor_idx += 1


        output_letter = self.ukw.route_signal(output_letter)  # Reflect signal

        rotor_idx = 2
        for rotor in reversed(self.rotors):  # After reflection
            print('Before correction > ', output_letter)
            output_letter = self.correct_position(output_letter, rotor_idx, 'back')
            print('After correction > ', output_letter)
            output_letter = rotor.route_signal(output_letter, 'back')

            rotor_idx -= 1

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
                                rotors['UKW-B'])

#"""
output = ''
for letter in 'A':
    output += enigma.button_press(letter)

print('\nOutput: ', output, '\n')

enigma.set_rotor_pos([0,0,0])

output2 = ''
for letter in output:
    output2 += enigma.button_press(letter)

print('\nOutput: ', output2)
#"""
