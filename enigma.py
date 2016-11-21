from tkinter import messagebox

from historical import Enigma1
from rotor import Rotor


class Enigma:
    def __init__(self, reflector, rotors):
        self.use_reflector(reflector)
        self.use_rotors(rotors)
        self.last_output = ''

    def get_rotors(self):
        return_list = [self.reflector.label]
        return_list.extend([rotor.label for rotor in self.rotors])
        return return_list

    def use_rotors(self, rotors):
        if all([rotor in Enigma1.rotors for rotor in rotors]):
            self.rotors = [Rotor(Enigma1.rotors[rotor]) for rotor in rotors]
        else:
            messagebox.showwarning('Invalid rotor', 'Some of rotors are not \n'
                                                    'valid, please try again...')

    def use_reflector(self, reflector):
        if reflector in Enigma1.rotors:
            self.reflector = Rotor(Enigma1.rotors[reflector])
        else:
            messagebox.showwarning('Invalid reflector', 'Invalid reflector,'
                                                        ' please try '
                                                        'again...')

    def set_offsets(self, offsets):
        for rotor, offset in zip(self.rotors, offsets):
            rotor.set_offset(offset)

    def rotate_primary(self, places=1):
        rotate_next = False
        index = 0
        for rotor in self.rotors:
            if rotate_next or index == 0:
                rotate_next = rotor.rotate(places)
            index += 1

    def prt_positions(self):
        """print('Rotor positions >', self.rotors[0].position,
              self.rotors[1].position, self.rotors[2].position)
        """
        output = '%s %s %s' % (self.rotors[2].back_board,
                                              self.rotors[1].back_board,
                                              self.rotors[0].back_board)

        if self.last_output != output:
            print(output)

        self.last_output = output

    def button_press(self, letter):
        self.rotate_primary()
        output = letter

        for rotor in self.rotors:
            output = rotor.forward(output)

        output = self.reflector.forward(output)

        for rotor in reversed(self.rotors):
            output = rotor.backward(output)

        return output
