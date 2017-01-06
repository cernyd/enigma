from tkinter import messagebox

from enigma_components.rotor_factory import RotorFactory


class Enigma:
    """Enigma machine object emulating all mechanical processes in the real enigma machine"""
    def __init__(self, reflector=None, rotors=None, config_data=None):
        self._reflector = None
        self.reflector = reflector
        self._rotors = []
        self.rotors = rotors  # Calling property
        self._plugboard = []
        self.last_output = ''  # To avoid sending the same data from rotor position class

    @property
    def plugboard(self):
        return self._plugboard

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

        self._plugboard = plugboard_pairs

    @property
    def reflector_label(self):
        return self.reflector.label

    @property
    def rotor_labels(self):
        """Returns rotor type ( label ), for the rotor order window."""
        return [rotor.label for rotor in self._rotors]

    @property
    def rotor_turnovers(self):
        return [rotor.turnover for rotor in self._rotors]

    @property
    def rotors(self):
        return self._rotors

    @rotors.setter
    def rotors(self, labels):
        """Sets rotors"""
        self._rotors = []
        for label in labels:
            self._rotors.append(RotorFactory.produce('Enigma1', 'rotor', label))

    @property
    def positions(self):
        return [rotor.position for rotor in self._rotors]

    @positions.setter
    def positions(self, positions):
        for position, rotor in zip(positions, self._rotors):
            rotor.position = position

    @property
    def reflector(self):
        return self._reflector

    @reflector.setter
    def reflector(self, label):
        print('Base called!')
        self._reflector = RotorFactory.produce('Enigma1', 'reflector', label)

    @property
    def ring_settings(self):
        return [rotor.ring_setting for rotor in self.rotors]

    @ring_settings.setter
    def ring_settings(self, offsets):
        for rotor, setting in zip(self.rotors, offsets):
            rotor.ring_setting = setting

    def _plugboard_route(self, letter):
        neighbour = []
        for pair in self._plugboard:
            if letter in pair:
                neighbour.extend(pair)
                neighbour.remove(letter)
                return neighbour[0]
        return letter  # If no connection found

    def rotate_primary(self, places=1):
        rotate_next = False
        index = 0
        for rotor in reversed(self._rotors):
            if rotate_next or index == 0:
                rotate_next = rotor.rotate(places)
            index += 1

    def button_press(self, letter):
        self.rotate_primary()
        output = self._plugboard_route(letter)

        for rotor in reversed(self._rotors):
            output = rotor.forward(output)

        output = self.reflector.reflect(output)

        for rotor in self._rotors:
            output = rotor.backward(output)

        output = self._plugboard_route(output)

        return output

    def dump_config(self):
        """Dumps the whole enigma data config"""
        return dict(plugboard=self._plugboard,
                    reflector=self.reflector.dump_config(),
                    rotors=[rotor.dump_config() for rotor in self._rotors])

    def load_config(self, data):
        """Loads everything from the data config"""
        self.plugboard = data['plugboard']
        self._reflector.config(**data['reflector'])
        for rotor, config in zip(self._rotors, data['rotors']):
            rotor.config(** config)


class TkEnigma(Enigma):
    """Enigma adjusted for Tk rotor lock"""
    def __init__(self, master, *config):
        Enigma.__init__(self, *config)
        self.master = master

    def rotate_primary(self, places=1):
        if not self.master.rotor_lock:
            Enigma.rotate_primary(self, places)

    @Enigma.reflector.setter
    def reflector(self, label):
        try:
            Enigma.reflector.fset(self, label)
        except AttributeError as err:
            print(err)
            messagebox.showwarning('Invalid reflector', 'Invalid reflector,'
                                                        ' please try '
                                                        'again...')
    @Enigma.rotors.setter
    def rotors(self, labels):
        """Adds a visual error feedback ( used only in the tk implementation"""
        try:
            Enigma.rotors.fset(self, labels)
        except AttributeError as err:
            print(err)
            messagebox.showwarning('Invalid rotor', 'Some of rotors are not \n'
                                                    'valid, please try again...')
