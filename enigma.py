from tkinter import messagebox

from misc import Enigma1
from rotor import Rotor


class Enigma:
    def __init__(self, reflector, rotors):
        self.reflector = reflector
        self.rotors = rotors  # Calling property
        self._plugboard = []
        self.last_output = ''

    def plugboard_route(self, letter):
        """Routes a letter trough the plugboard"""
        neighbour = []
        for pair in self._plugboard:
            if letter in pair:
                neighbour.extend(pair)
                neighbour.remove(letter)
                return neighbour[0]
        return letter # If no connection found

    @property
    def plugboard(self):
        return self._plugboard

    @plugboard.setter
    def plugboard(self, pairs):
        """Sets up plugboard pairs for the plugboard routing"""
        assert(len(pairs) <= 13), "Invalid number of pairs!"
        used = []
        plugboard_pairs = []
        for pair in pairs:
            for letter in pair:
                assert(letter not in used), "A letter can only be wired once!"
                used.append(letter)
            plugboard_pairs.append(pair)

        self._plugboard = plugboard_pairs

    @property
    def rotor_labels(self):
        """Returns rotor type ( label ), for the rotor order window."""
        return_list = [self.reflector.label]
        return_list.extend([rotor.label for rotor in self._rotors])
        return return_list

    @property
    def rotors(self):
        return self._rotors

    @rotors.setter
    def rotors(self, rotors):
        """Takes rotor labels and gets the rotors from historical rotors if possible,
        shows a warning if any rotor is invalid"""
        temp = []
        if all([rotor in Enigma1.rotors for rotor in rotors]):
            for rotor in rotors:
                temp.append(Rotor(*Enigma1.rotors[rotor]))
        else:
            messagebox.showwarning('Invalid rotor', 'Some of rotors are not \n'
                                                    'valid, please try again...')
        self._rotors = temp[:]

    @property
    def reflector(self):
        return self._reflector

    @reflector.setter
    def reflector(self, reflector):
        """Takes a reflector label and gets the reflector from historical reflectors,
        shows a warning if the rotor label is invalid"""
        if reflector in Enigma1.rotors:
            self._reflector = Rotor(Enigma1.rotors[reflector])
        else:
            messagebox.showwarning('Invalid reflector', 'Invalid reflector,'
                                                        ' please try '
                                                        'again...')

    @property
    def ring_settings(self):
        """Returns ring settings of all the rotors"""
        return [rotor.ring_setting for rotor in self.rotors[::-1]]

    @ring_settings.setter
    def ring_settings(self, offsets):
        """Takes three numbers as ring settings and applies them to the rotors"""
        for rotor, setting in zip(self.rotors, offsets):
            rotor.ring_setting = setting

    @property
    def positions(self):
        """Prints rotor wiring ( the offset is visible ), this can visualise the
        rotors turning"""
        output = '%s %s %s' % (self.rotors[2].back_board,
                                              self.rotors[1].back_board,
                                              self.rotors[0].back_board)

        if self.last_output != output:  # Wiring only printed if anything changed
            return output

        self.last_output = output

    def rotate_primary(self, places=1):
        """Rotates the first rotor, handles rotor turnovers"""
        rotate_next = False
        index = 0
        for rotor in self._rotors:
            if rotate_next or index == 0:
                rotate_next = rotor.rotate(places)
            index += 1

    def button_press(self, letter):
        """Takes a letter and simulates enigma encryption, returns a letter that would
        be shown on the enigma lightbulb board"""
        self.rotate_primary()
        output = letter

        output = self.plugboard_route(output)

        for rotor in self._rotors:
            output = rotor.forward(output)

        output = self.reflector.forward(output)

        for rotor in reversed(self._rotors):
            output = rotor.backward(output)

        output = self.plugboard_route(output)

        return output
