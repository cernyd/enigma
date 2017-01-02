import xml.etree.ElementTree as ET
from functools import wraps
from os import getcwd
from string import ascii_uppercase as alphabet


def data_interface(data_type, rotor_type=None, label=None):
    print(getcwd())
    extra_info = rotor_type, label
    data = ET.parse('data\historical_data.xml').getroot().find(
        data_type)
    if all(extra_info):
        for rotor in data.find(rotor_type):
            if rotor.attrib['label'] == label:
                return rotor.attrib
    else:
        assert (not any(extra_info)), 'Not enough data to return rotor cfg!'
        return data


class RotorFactory:
    """Factory for creating various enigma Rotor/Reflector objects"""
    def __new__(cls):
        raise NotImplementedError('This class was not intended for instantiation!')

    @classmethod
    def produce(cls, model, rotor_type, label):
        """Creates and returns new object based on input"""
        cfg = data_interface(model, rotor_type, label)

        if cfg:
            if rotor_type == 'rotor':
                return  Rotor(**cfg)
            elif rotor_type == 'reflector':
                return  Reflector(**cfg)
        else:
            raise AttributeError('No configuration found for "%s" > '
                                 '"%s" > "%s"!' % (model, rotor_type, label))


class RotorBase:
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
                raise AttributeError('Invalid attribute "%s"!' % attr)
            value = attrs.get(attr)
            if value:
                setattr(self, attr, value)

    def dump_config(self):
        """Dumps rotor configuration data"""
        cfg = {}
        for attr in self.valid_cfg:
            cfg[attr] = self.__dict__[attr]
        return cfg


class Reflector(RotorBase):
    """Reflector class, used to """

    def reflect(self, letter):
        """Reflects letter back"""
        return self._route_forward(letter)


def compensate(func):
    @wraps(func)
    def wrapper(self, letter):
        relative_input = self.relative_board[alphabet.index(letter)]
        return alphabet[
            self.relative_board.index(func(self, relative_input))]

    return wrapper


class Rotor(RotorBase):
    """Inherited from RotorBase, adds rotation and ring setting functionality"""

    def __init__(self, turnover=tuple(), **cfg):
        RotorBase.__init__(self, **cfg, valid_cfg=('position_ring', 'turnover',
                                                   'relative_board'))
        self.position_ring, self.relative_board = [alphabet] * 2
        self.turnover = turnover
        self._last_position = ''

    def _route_backward(self, letter):
        """Routes letters from back board to front board"""
        return alphabet[self.back_board.index(letter)]

    @compensate
    def forward(self, letter):
        """Routes letter from front to back"""
        return self._route_forward(letter)

    @compensate
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