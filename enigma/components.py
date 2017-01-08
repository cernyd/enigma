from functools import wraps
from string import ascii_uppercase as alphabet
from cfg_handler import Config


class RotorFactory:
    """Factory for creating various enigma Rotor/Reflector objects"""
    def __init__(self, cfg_path):
        self.cfg = Config(cfg_path)

    def produce(self, model, rotor_type, label):
        """Creates and returns new object based on input"""
        for enigma in [self.cfg.get_data('enigma')]:
            if enigma['model'] == model:
                model = enigma
                break

        cfg = None
        for item in model.find(rotor_type, 'SUBATTRS'):
            if item['label'] == label:
                cfg = item.attrib
                cfg.update(label=label)
                break

        assert cfg, "No configuration found!"
        if rotor_type == 'rotors':
            return Rotor(**cfg)
        elif rotor_type == 'reflectors':
            return Reflector(**cfg)


class Enigma:
    """Enigma machine object emulating all mechanical processes in the real
    enigma machine"""
    def __init__(self, reflector=None, rotors=None):
        self.rotor_factory = RotorFactory(['enigma', 'historical_data.xml'])
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
        assert (len(pairs) <= 13), "Invalid number of pairs!"

        used = []
        plugboard_pairs = []
        for pair in pairs:
            for letter in pair:
                assert (letter not in used), "A letter can only be wired once!"
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
    def rotors(self):
        return self._rotors

    @rotors.setter
    def rotors(self, labels):
        """Sets rotors"""
        self._rotors = []
        for label in labels:
            self._rotors.append(self.rotor_factory.produce('Enigma1', 'rotors', label))

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
        self._reflector = self.rotor_factory.produce('Enigma1', 'reflectors', label)

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

    def _rotate_primary(self, places=1):
        rotate_next = False
        index = 0
        for rotor in reversed(self._rotors):
            if rotate_next or index == 0:
                rotate_next = rotor.rotate(places)
            index += 1

    def button_press(self, letter):
        self._rotate_primary()
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
            rotor.config(**config)


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
    relative output to absolute output."""
    @wraps(func)
    def wrapper(self, letter):
        relative_input = self.relative_board[alphabet.index(letter)]
        return alphabet[self.relative_board.index(func(self, relative_input))]
    return wrapper


class Rotor(_RotorBase):
    """Inherited from RotorBase, adds rotation and ring setting functionality"""
    def __init__(self, turnover: str, **cfg):
        _RotorBase.__init__(self, **cfg, valid_cfg=('position_ring', 'turnover',
                                                    'relative_board'))
        self.turnover = turnover
        self.position_ring, self.relative_board = [alphabet] * 2
        self._last_position = ''

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
        self.change_rotor_offset(places)
        return self._did_turnover()

    def _did_turnover(self):
        """Checks if the next position should turn by one place."""
        if (self._last_position, self.position) == self.turnover:
            return True
        elif (self.position, self._last_position) == self.turnover:
            return True
        return False

    def change_board_offset(self, board, places=1):
        """Changes offset of a specified board."""
        old_val = getattr(self, board)
        new_val = old_val[places:] + old_val[:places]
        setattr(self, board, new_val)

    def change_rotor_offset(self, places=1):
        """Sets rotor offset relative to the enigma"""
        self._last_position = self.position
        for board in 'relative_board', 'position_ring':
            self.change_board_offset(board, places)

    @property
    def position(self):
        return self.relative_board[0]

    @position.setter
    def position(self, position):
        while self.position_ring[0] != position:
            self.change_rotor_offset()

    @property
    def ring_setting(self):
        return self.position_ring[self.relative_board.index('A')]

    @ring_setting.setter
    def ring_setting(self, setting):
        """Sets rotor indicator offset relative to the internal wiring"""
        while self.ring_setting != setting:
            self.change_board_offset('relative_board')
