from tkinter import messagebox

from misc import Enigma1
from rotor import Rotor


class Enigma:
    def __init__(self, reflector, rotors):
        self.use_reflector(reflector)
        self.use_rotors(rotors)
        self.plugboard_pairs = []
        self.last_output = ''

    def plugboard_route(self, letter):
        """Routes a letter trough the plugboard"""
        neighbour = []
        for pair in self.plugboard_pairs:
            if letter in pair:
                neighbour.extend(pair)
                neighbour.remove(letter)
                return neighbour[0]
        return letter # If no connection found

    def set_plugboard(self, pairs):
        """Sets up plugboard pairs for the plugboard routing"""
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
        """Returns ring settings of all the rotors"""
        return [rotor.ring_setting for rotor in self.rotors[::-1]]

    def get_rotors(self):
        """Returns rotor type ( label ), for the rotor order window."""
        return_list = [self.reflector.label]
        return_list.extend([rotor.label for rotor in self.rotors])
        return return_list

    def use_rotors(self, rotors):
        """Takes rotor labels and gets the rotors from historical rotors if possible,
        shows a warning if any rotor is invalid"""
        if all([rotor in Enigma1.rotors for rotor in rotors]):
            self.rotors = []
            for rotor in rotors:
                self.rotors.append(Rotor(*Enigma1.rotors[rotor]))
        else:
            messagebox.showwarning('Invalid rotor', 'Some of rotors are not \n'
                                                    'valid, please try again...')

    def use_reflector(self, reflector):
        """Takes a reflector label and gets the reflector from historical reflectors,
        shows a warning if the rotor label is invalid"""
        if reflector in Enigma1.rotors:
            self.reflector = Rotor(Enigma1.rotors[reflector])
        else:
            messagebox.showwarning('Invalid reflector', 'Invalid reflector,'
                                                        ' please try '
                                                        'again...')

    def set_ring_settings(self, offsets):
        """Takes three numbers as ring settings and applies them to the rotors"""
        for rotor, setting in zip(self.rotors, offsets):
            rotor.set_ring_setting(setting)

    def rotate_primary(self, places=1):
        """Rotates the first rotor, handles rotor turnovers"""
        rotate_next = False
        index = 0
        for rotor in self.rotors:
            if rotate_next or index == 0:
                rotate_next = rotor.rotate(places)
            index += 1

    def prt_positions(self):
        """Prints rotor wiring ( the offset is visible ), this can visualise the
        rotors turning"""
        output = '%s %s %s' % (self.rotors[2].back_board,
                                              self.rotors[1].back_board,
                                              self.rotors[0].back_board)

        if self.last_output != output:  # Wiring only printed if anything changed
            print(output)

        self.last_output = output

    def button_press(self, letter):
        """Takes a letter and simulates enigma encryption, returns a letter that would
        be shown on the enigma lightbulb board"""
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
