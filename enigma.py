from tkinter import messagebox
from rotor_factory import RotorFactory
from os import system


class Enigma:
    """Enigma machine object emulating all mechanical processes in the real enigma machine"""
    def __init__(self, reflector=None, rotors=None, master=None, config_data=None):
        """
        :param reflector: Reflector label, reflector object will be created automatically
        :param rotors: Three rotor labels, objects will be created automatically
        """
        self.reflector = reflector
        self.rotors = rotors  # Calling property
        self.__plugboard = []
        self.last_output = ''  # To avoid sending the same data from rotor position class

        if master:
            self.master = master

    def print_rotors(self):
        system('cls')
        length = len(self.rotors[0].relative_board)
        print('I')
        print('-' * length)
        print(self.rotors[0].position_ring)
        print(self.rotors[0].relative_board)
        print(self.rotors[0].back_board)
        print(self.rotors[0].relative_board)
        print('-' * length)
        print('II')
        print('-'*length)
        print(self.rotors[1].position_ring)
        print(self.rotors[1].relative_board)
        print(self.rotors[1].back_board)
        print(self.rotors[1].relative_board)
        print('-' * length)
        print('III')
        print('-' * length)
        print(self.rotors[2].position_ring)
        print(self.rotors[2].relative_board)
        print(self.rotors[2].back_board)
        print(self.rotors[2].relative_board)
        print('-' * length)

    @property
    def plugboard(self):
        return self.__plugboard

    @plugboard.setter
    def plugboard(self, pairs):
        assert(len(pairs) <= 13), "Invalid number of pairs!"

        used = []
        plugboard_pairs = []
        for pair in pairs:
            for letter in pair:
                assert(letter not in used), "A letter can only be wired once!"
                used.append(letter)
            plugboard_pairs.append(pair)

        self.__plugboard = plugboard_pairs

    @property
    def rotor_labels(self):
        """Returns rotor type ( label ), for the rotor order window."""
        return_list = [self.reflector.label]
        return_list.extend([rotor.label for rotor in self._rotors])
        return return_list

    @property
    def rotor_turnovers(self):
        return_list = [self.reflector.turnover]
        return_list.extend([rotor.turnover for rotor in self._rotors])
        return return_list

    @property
    def rotors(self):
        return self._rotors

    @rotors.setter
    def rotors(self, labels):
        self._rotors = []
        try:
            for label in labels:
                self._rotors.append(RotorFactory.produce('Enigma1', 'rotor', label))
        except AttributeError:
            messagebox.showwarning('Invalid rotor', 'Some of rotors are not \n'
                                                    'valid, please try again...')

    @property
    def positions(self):
        output = '%s %s %s' % (self.rotors[2], self.rotors[1], self.rotors[0])

        if self.last_output != output:  # Wiring only printed if anything changed
            return output

        self.last_output = output

    @property
    def reflector(self):
        return self._reflector

    @reflector.setter
    def reflector(self, label):
        try:
            self._reflector = RotorFactory.produce('Enigma1', 'reflector', label)
        except AttributeError:
            messagebox.showwarning('Invalid reflector', 'Invalid reflector,'
                                                        ' please try '
                                                        'again...')

    @property
    def ring_settings(self):
        return [rotor.ring_setting for rotor in self.rotors[::-1]]

    @ring_settings.setter
    def ring_settings(self, offsets):
        for rotor, setting in zip(self.rotors, offsets):
            rotor.ring_setting = setting

    def plugboard_route(self, letter):
        neighbour = []
        for pair in self.__plugboard:
            if letter in pair:
                neighbour.extend(pair)
                neighbour.remove(letter)
                return neighbour[0]
        return letter  # If no connection found

    def rotate_primary(self, places=1):
        if self.master:
            if not self.master.rotor_lock:
                rotate_next = False
                index = 0
                for rotor in self._rotors:
                    if rotate_next or index == 0:
                        rotate_next = rotor.rotate(places)
                    index += 1

    def button_press(self, letter):
        self.rotate_primary()
        self.print_rotors()
        output = letter
        output = self.plugboard_route(output)

        for rotor in self._rotors:
            output = rotor.forward(output)

        output = self.reflector.forward(output)

        for rotor in reversed(self._rotors):
            output = rotor.backward(output)

        output = self.plugboard_route(output)

        return output

    # def dump_config(self):
    #     """Dumps the whole enigma data config"""
    #     return dict(plugboard=self.__plugboard,
    #                 reflector=self.reflector.dump_config(),
    #                 rotors=[rotor.dump_config() for rotor in self._rotors])
    #
    # def load_config(self, data):
    #     """Loads everything from the data config"""
    #     self.plugboard = data['plugboard']
    #     self._reflector = Rotor(config_data=data['reflector'])
    #     self._rotors = [Rotor(config_data=config) for config in data['rotors']]
