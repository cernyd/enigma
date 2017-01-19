from functools import wraps
from string import ascii_uppercase as alphabet
from cfg_handler import Config


class RotorFactory:
    """Factory for creating various enigma Rotor/Reflector objects"""
    def __init__(self, cfg_path, model):
        self.cfg = Config(cfg_path)
        self.base_path = f"enigma[@model='{model}']"
        self.model = model
        self.rotors = [item['label'] for item in self.cfg.get_data([self.base_path, 'rotors'], 'SUBATTRS')]
        self.reflectors = [item['label'] for item in self.cfg.get_data([self.base_path, 'reflectors'], 'SUBATTRS')]
        self.layout = []
        [self.layout.append(row['values']) for row in
         self.cfg.get_data('layout', 'SUBATTRS')]
        self.labels = []
        [self.labels.extend(row['values']) for row in
         self.cfg.get_data('labels', 'SUBATTRS')]


    def produce(self, model, rotor_type, label):
        """Creates and returns new object based on input"""
        cfg = self.cfg.get_data([self.base_path, rotor_type], 'SUBATTRS')

        match = False
        for item in cfg:
            if item['label'] == label:
                cfg = item
                match = True
                break

        err_msg = f"No configuration found for label \"{label}\"!"
        assert match, err_msg
        if rotor_type == 'rotors':
            return Rotor(**cfg)
        elif rotor_type == 'reflectors':
            return Reflector(**cfg)


class _SteppingMechanism:
    def __init__(self, rotors):
        self._rotors = rotors

    def step_primary(self, places):
        pass


class RatchetStepper(_SteppingMechanism):
    def step_primary(self, places):
        step_next = False
        index = 0
        for rotor in reversed(self._rotors):
            if index == 0:
                if places < 0:
                    rotor.rotate(places)
                if rotor.position in rotor.turnover:
                    step_next = True
                if places > 0:
                    rotor.rotate(places)
            elif index == 1 and rotor.position in rotor.turnover:
                rotor.rotate(places)
                step_next = True
            elif step_next:
                rotor.rotate(places)
                step_next = False

            index += 1


class _EnigmaBase:
    def __init__(self, reflector, rotors, stator):
        self._stator = stator
        self._rotors = rotors
        self._reflector = reflector
        self._stepping_mechanism = None

    @property
    def rotor_labels(self):
        """Returns rotor type ( label ), for the rotor order window."""
        return [rotor.label for rotor in self._rotors]

    @property
    def rotors(self):
        return self._rotors

    @rotors.setter
    def rotors(self, rotors):
        """Sets rotors"""
        self._rotors = rotors

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
    def reflector(self, reflector):
        self._reflector = reflector

    @property
    def ring_settings(self):
        return [rotor.ring_setting for rotor in self.rotors]

    @ring_settings.setter
    def ring_settings(self, offsets):
        for rotor, setting in zip(self.rotors, offsets):
            rotor.ring_setting = setting

    def step_primary(self, places=1):
        self._stepping_mechanism.step(places)

    def button_press(self, letter):
        pass

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
            rotor.config(**config)


class Enigma1(_EnigmaBase):
    def __init__(self, plugboard, *args):
        _EnigmaBase.__init__(self, *args)
        self.plugboard = plugboard

    @property
    def plugboard(self):
        return self._plugboard

    @plugboard.setter
    def plugboard(self, pairs):
        assert (len(pairs) <= 13), "Invalid number of pairs!"

        used = []
        plugboard_pairs = []
        for pair in pairs:
            for letter in pair:
                assert (letter not in used), "A letter can only be wired once!"
                used.append(letter)
            plugboard_pairs.append(pair)

        self._plugboard = plugboard_pairs

    def _plugboard_route(self, letter):
        neighbour = []
        for pair in self._plugboard:
            if letter in pair:
                neighbour.extend(pair)
                neighbour.remove(letter)
                return neighbour[0]
        return letter  # If no connection found

    def button_press(self, letter):
        self.step_primary(1)
        output = self._plugboard_route(letter)

        for rotor in reversed(self._rotors):
            output = rotor.forward(output)

        output = self.reflector.reflect(output)

        for rotor in self._rotors:
            output = rotor.backward(output)

        output = self._plugboard_route(output)

        return output


class EnigmaM3(Enigma1):
    def __init__(self, *args):
        Enigma1.__init__(self, *args)
        assert len(self._rotors) == 3, "Invalid number of rotors!"
        self.stepping_mechanism = RatchetStepper(self._rotors)


class EnigmaM4(Enigma1):
    def __init__(self, *args):
        Enigma1.__init__(self, *args)
        assert len(self._rotors) == 4, "Invalid number of rotors!"
        self.stepping_mechanism = RatchetStepper(self._rotors[1:])


class _RotorBase:
    """Base class for Rotors and Reflectors"""
    def __init__(self, label='', back_board='', valid_cfg=tuple()):
        """All parameters except should be passed in **config, valid_cfg is a
        tuple of additional configuration data for config loading and dumping"""
        self.valid_cfg = ['back_board', 'label']
        self.valid_cfg.extend(valid_cfg)

        self.back_board = back_board
        self.label = label

    def _route_forward(self, letter):
        """Routes letters from front board to back board"""
        return self.back_board[alphabet.index(letter)]

    def config(self, **attrs):
        """Loads rotor configuration data"""
        for attr in attrs.keys():
            if attr not in self.valid_cfg:
                raise AttributeError(f'Invalid attribute "{attr}"!')
            value = attrs.get(attr)
            if value:
                setattr(self, attr, value)

    def dump_config(self):
        """Dumps rotor configuration data"""
        cfg = {}
        for attr in self.valid_cfg:
            cfg[attr] = self.__dict__[attr]
        return cfg


class Reflector(_RotorBase):
    """Reflector class, used to """

    def reflect(self, letter):
        """Reflects letter back"""
        return self._route_forward(letter)


def _compensate(func):
    """Converts input to relative input and
    relative output to absolute output, does some assertions too."""
    @wraps(func)
    def wrapper(self, letter):
        letter = str(letter).upper()
        if not str(letter) in alphabet:
            raise AssertionError(f"Input \"{str(letter)}\" not single a letter!")
        elif len(letter) != 1:
            raise AssertionError("Length of \"{str(letter)}\" is not 1!")
        relative_input = self.relative_board[alphabet.index(letter)]
        return alphabet[self.relative_board.index(func(self, relative_input))]
    return wrapper


class Rotor(_RotorBase):
    """Inherited from RotorBase, adds rotation and ring setting functionality"""
    def __init__(self, label, turnover, back_board):
        _RotorBase.__init__(self, label, back_board,
                            valid_cfg=('position_ring', 'turnover', 'relative_board'))

        self.turnover = turnover
        self.position_ring, self.relative_board = [alphabet] * 2

    def _route_backward(self, letter):
        """Routes letters from back board to front board"""
        return alphabet[self.back_board.index(letter)]

    @_compensate
    def forward(self, letter):
        """Routes letter from front to back"""
        return self._route_forward(letter)

    @_compensate
    def backward(self, letter):
        """Routes letter from back to front"""
        return self._route_backward(letter)

    def rotate(self, places=1):
        """Rotates rotor by one x places, returns True if the next rotor should
        be turned over"""
        for board in 'relative_board', 'position_ring':
            self._change_board_offset(board, places)

    def _change_board_offset(self, board, places=1):
        """Changes offset of a specified board."""
        old_val = getattr(self, board)
        new_val = old_val[places:] + old_val[:places]
        setattr(self, board, new_val)

    @property
    def position(self):
        return self.position_ring[0]

    def _generic_setter(self, message, uptodate_value, target_value, update_action):
        assert str(target_value) in alphabet, message % str(target_value)
        while uptodate_value() != target_value:
            update_action()

    @position.setter
    def position(self, position):
        """Sets rotor to target position"""
        self._generic_setter("Invalid position\"%s\"!", lambda: getattr(self, 'position'),
                             position, self.rotate)

    @property
    def ring_setting(self):
        return self.position_ring[self.relative_board.index('A')]

    @ring_setting.setter
    def ring_setting(self, setting):
        """Sets rotor indicator offset relative to the internal wiring"""
        self._generic_setter("Invalid ring setting \"%s\"!", lambda: getattr(self, 'ring_setting'),
                             setting, lambda: self._change_board_offset('relative_board'))
