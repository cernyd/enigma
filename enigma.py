from tkinter import messagebox

from historical import Enigma1
from rotor import Rotor


class Enigma:
    def __init__(self, reflector, rotors):
        self.use_reflector(reflector)
        self.use_rotors(rotors)
        self.plugboard_pairs = []
        self.last_output = ''

    def plugboard_route(self, letter):
        neighbour = []
        for pair in self.plugboard_pairs:
            if letter in pair:
                neighbour.extend(pair)
                neighbour.remove(letter)
                return neighbour[0]
        return letter # If no connection found

    def set_plugboard(self, pairs):
        assert(len(pairs) <= 13), "Invalid number of pairs!"
        used = []
        plugboard_pairs = []
        for pair in pairs:
            for letter in pair:
                assert(letter not in used), "A letter can only be wired once!"
                used.append(letter)
            plugboard_pairs.append(pair)

        self.plugboard_pairs = plugboard_pairs

    def get_ring_settings(self):
        return [rotor.ring_setting for rotor in self.rotors[::-1]]

    def get_rotors(self):
        return_list = [self.reflector.label]
        return_list.extend([rotor.label for rotor in self.rotors])
        return return_list

    def use_rotors(self, rotors):
        if all([rotor in Enigma1.rotors for rotor in rotors]):
            self.rotors = []
            for rotor in rotors:
                self.rotors.append(Rotor(*Enigma1.rotors[rotor]))
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

    def set_ring_settings(self, offsets):
        for rotor, setting in zip(self.rotors, offsets):
            rotor.set_ring_setting(setting)

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

        if self.last_output != output:  # Wiring only printed if anything changed
            print(output)

        self.last_output = output

    def button_press(self, letter):
        self.rotate_primary()
        output = letter

        output = self.plugboard_route(output)

        for rotor in self.rotors:
            output = rotor.forward(output)

        output = self.reflector.forward(output)

        for rotor in reversed(self.rotors):
            output = rotor.backward(output)

        output = self.plugboard_route(output)

        return output
