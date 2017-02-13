from string import ascii_uppercase as alphabet
from itertools import permutations
from cfg_handler import Config
from functools import wraps
import unittest

# UNIT TEST

class TestEnigma(unittest.TestCase):
    """Used to test if enigma class behaves like the real life counterpart"""
    model = ''
    cfg_path = []

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.cfg = Config(TestEnigma.cfg_path)
        self.cfg.focus_buffer('test_cfg')
        self.subject = None
        self.enigma_factory = EnigmaFactory(['enigma', 'historical_data.xml'])
        self.reset_subject()

    def reset_subject(self):
        buffer = self.cfg.get_data('default_cfg')
        self.subject = self.enigma_factory.produce('EnigmaM3')

    def test_encrypt_decrypt(self):
        """Tests if encryption and decryption are working properly"""
        buffer = self.cfg.get_data('test_encrypt_decrypt')
        for test in permutations(['encrypted', 'decrypted']):
            self.reset_subject()
            output = ''
            for letter in buffer[test[0]]:
                output += self.subject.button_press(letter)
            self.assertEqual(output, buffer[test[1]], f'Failed to '
                                                             f'{test[1][:-2]}!')
        with self.assertRaises(AssertionError):
            self.subject.button_press(18)

    def test_rotors(self):
        """Tests if rotors are assigned properly"""
        self.reset_subject()
        rotors = self.cfg.get_data('test_rotors')['rotors']
        self.subject.rotors = rotors
        self.assertEqual(self.subject.rotor_labels, rotors,
                         'Invalid rotor order assigned!')

    def test_positions(self):
        """Tests if rotor positions are set properly"""
        self.reset_subject()
        positions = self.cfg.get_data('test_positions')['positions']
        self.subject.positions = positions
        self.assertEqual(self.subject.positions, positions,
                         'Positions assigned in wrong order!')
        with self.assertRaises(AssertionError):
            self.subject.positions = 14651, 'garbage', -15

    def test_reflector(self):
        """Tests if the reflector is set properly"""
        self.reset_subject()
        reflector = self.cfg.get_data('test_reflector')['reflector']
        self.subject.reflector = reflector
        self.assertEqual(self.subject.reflector_label, reflector,
                         'Invalid rotor assigned!')
        with self.assertRaises(AssertionError):
            self.subject.reflector = 'garbage_input'

    def test_ring_settings(self):
        """Tests if ring settings are set properly"""
        self.reset_subject()
        ring_settings = self.cfg.get_data('test_ring_settings')['ring_settings']
        self.subject.ring_settings = ring_settings
        self.assertEqual(self.subject.ring_settings, ring_settings,
                         'Invalid ring settings assigned!')
        with self.assertRaises(AssertionError):
            self.subject.ring_settings = [12, 'garbage_input', 798715]

    def test_plugboard(self):
        """Checks if plugboard pairs are set propertly"""
        self.reset_subject()
        plug_pairs = self.cfg.get_data('test_plugboard')['pairs']
        self.subject.plugboard = plug_pairs
        self.assertEqual(self.subject.plugboard, plug_pairs, 'Invalid plugboard'
                                                             ' pairs assigned!')
        with self.assertRaises(AssertionError):
            self.subject.plugboard = 'garbage_input'


    # def test_cfg_io(self):
    #     """Tests if rotor data is dumped and loaded correctly"""
    #
    # def test_enigma_cfg_io(self):
    #     """Tests if enigma data is dumped and loaded correctly"""


# GENERIC COMPONENTS

class WiredPairs:
    """Returns the other letter from pairs if one letter is given.
    IS FLEXIBLE!"""
    def __init__(self, pairs=''):
        self._pairs = pairs

    @property
    def pairs(self):
        return self._pairs

    @pairs.setter
    def pairs(self, pairs):
        assert (len(pairs) <= 13), "Invalid number of pairs!"

        used = []
        new_pairs = []
        for pair in pairs:
            for letter in pair:
                assert (letter not in used), "A letter can only be wired once!"
                used.append(letter)
            new_pairs.append(pair)

        self._pairs = new_pairs

    def pairs_route(self, letter):
        neighbour = []
        for pair in self._pairs:
            if letter in pair:
                neighbour.extend(pair)
                neighbour.remove(letter)
                return neighbour[0]
        return letter  # If no connection found


# HISTORICAL ENIGMA EXTENSIONS

class Uhr(WiredPairs):
    def __init__(self, pairs=''):
        WiredPairs.__init__(self, pairs)

    def pairs_route(self, letter):
        pass


# ENIGMA COMPONENTS

class EnigmaFactory:
    """Factory for producing enigma machines ( initialised more simply by
    choosing defaults from available config )"""
    def __init__(self, cfg_path):
        self._rotor_factory = RotorFactory(cfg_path)
        self._enigma_models = {'Enigma1': Enigma1, 'EnigmaM3': EnigmaM3}

    def produce(self, model, stator=None, rotors=None):
        """Produces an enigma machine given a specific model ( must be available
        in the speicified cfg_path )"""
        try:
            enigma_model = self._enigma_models[model]
        except KeyError:
            raise KeyError(f"No enigma model found for \"{model}\"!")

        reflector = None
        rotors = None
        stator = None

        return enigma_model(reflector, rotors, stator, [])


class Enigma:
    """Base for all enigma objects, has no plugboard, default rotor count for
    all enigma machines is 3."""
    rotor_count = 3

    def __init__(self, reflector, rotors, stator):
        self._stator = stator
        self._rotors = None
        self.rotors = rotors
        self._reflector = None
        self.reflector = reflector

    @property
    def rotor_count(self):
        return self.__class__.rotor_count

    def step_primary(self, places):
        """Steps primary rotor, other rotors will step too if in appropriate
        positions."""
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
        assert len(rotors) == self.rotor_count, "Invalid number of rotors!"
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

    def button_press(self, letter):
        self.step_primary(1)

        output = self._stator.forward(letter)

        for rotor in reversed(self._rotors):
            output = rotor.forward(output)

        output = self.reflector.reflect(output)

        for rotor in self._rotors:
            output = rotor.backward(output)

        return self._stator.backward(output)

    def dump_config(self):
        """Dumps the whole enigma data config"""
        return dict(reflector=self.reflector.dump_config(),
                    rotors=[rotor.dump_config() for rotor in self._rotors])

    def load_config(self, data):
        """Loads everything from the data config"""
        self._reflector.config(**data['reflector'])
        for rotor, config in zip(self._rotors, data['rotors']):
            rotor.config(**config)


class Enigma1(Enigma):
    """Adds plugboard functionality, compatible with all EnigmaM_ models
    except M4 ( Four rotors )"""
    def __init__(self, reflector, rotors, stator, plugboard_pairs=''):
        Enigma.__init__(self, stator, reflector, rotors)
        self._plugboard = WiredPairs(plugboard_pairs)

    @property
    def plugboard(self):
        """Plugboard routing pairs"""
        return self.plugboard.pairs

    @plugboard.setter
    def plugboard(self, pairs):
        self._plugboard.pairs = pairs

    def button_press(self, letter):
        """Wraps the base enigma routing with plugboard"""
        output = self._plugboard.pairs_route(letter)
        output = Enigma.button_press(self, output)
        return self._plugboard.pairs_route(output)

    def load_config(self, data):
        self._plugboard = data['plugboard']
        Enigma.load_config(self, data)

    def dump_config(self):
        config = Enigma.dump_config(self)
        config.update(plugboard=self._plugboard)
        return config


class EnigmaM3(Enigma1):
    """Name for the group of Enigma M1, M2 and M3 machines. All of them are
    practically identical"""


class EnigmaM4(EnigmaM3):
    """Navy version with four rotors, otherwise identical, UKW-D can be used
    instead. Thin reflectors are used, UKW-D can be used too if the extra rotor
    and thin reflector are replaced."""
    rotor_count = 4


# ROTOR COMPONENTS

class RotorFactory:
    """Factory for creating various enigma Rotor/Reflector objects"""
    def __init__(self, cfg_path):
        self.cfg = Config(cfg_path)
        self._base_path = "enigma[@model='{model}']"

    def produce(self, model, rotor_type, label):
        """Creates and returns new object based on input"""
        cfg = self.cfg.get_data([self._base_path.format(model=model), rotor_type],  'SUBATTRS')
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
        elif rotor_type == 'stators':
            return Stator(**cfg)


def _check_input(func):
    @wraps(func)
    def wrapper(self, letter):
        letter = str(letter).upper()
        if letter not in alphabet:
            raise AssertionError(
                f"Input \"{str(letter)}\" not single a letter!")
        elif len(letter) != 1:
            raise AssertionError("Length of \"{str(letter)}\" is not 1!")
        return func(self, letter)
    return wrapper


class _RotorBase:
    """Base class for Rotors and Reflectors"""
    def __init__(self, label, back_board, valid_cfg=tuple()):
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


class _Rotatable:
    """Adds the ability to change board offsets"""
    def _change_board_offset(self, board, places=1):
        """Changes offset of a specified board."""
        old_val = getattr(self, board)
        new_val = old_val[places:] + old_val[:places]
        setattr(self, board, new_val)


class Reflector(_RotorBase):
    """Reflector class, used to """
    @_check_input
    def reflect(self, letter):
        """Reflects letter back"""
        return self._route_forward(letter)


class Stator(_RotorBase):
    @_check_input
    def forward(self, letter):
        """Routes letter from front to back"""
        return self._route_forward(letter)

    @_check_input
    def backward(self, letter):
        """Routes letter from back to front"""
        return alphabet[self.back_board.index(letter)]


def _compensate(func):
    """Converts input to relative input and
    relative output to absolute output, does some assertions too."""
    @wraps(func)
    def wrapper(self, letter):
        relative_input = self.relative_board[alphabet.index(letter)]
        return alphabet[self.relative_board.index(func(self, relative_input))]
    return wrapper


class Rotor(Stator, _Rotatable):
    """Inherited from RotorBase, adds rotation and ring setting functionality"""
    def __init__(self, label,  back_board, turnover=''):
        Stator.__init__(self, label, back_board,
                            valid_cfg=('position_ring', '_Rotor_turnover', 'relative_board'))
        self._turnover = turnover
        self.position_ring, self.relative_board = [alphabet] * 2

    @_compensate
    def forward(self, letter):
        return Stator.forward(self, letter)

    @_compensate
    def backward(self, letter):
        return Stator.backward(self, letter)

    def rotate(self, places=1):
        """Rotates rotor by one x places, returns True if the next rotor should
        be turned over"""
        for board in 'relative_board', 'position_ring':
            self._change_board_offset(board, places)

    @property
    def turnover(self):
        return self._turnover

    @property
    def position(self):
        return self.position_ring[0]

    @position.setter
    def position(self, position):
        """Sets rotor to target position"""
        self._generic_setter("Invalid position\"%s\"!", lambda: getattr(self, 'position'),
                             position, self.rotate)

    def _generic_setter(self, message, uptodate_value, target_value, update_action):
        assert str(target_value) in alphabet, message % str(target_value)
        while uptodate_value() != target_value:
            update_action()

    @property
    def ring_setting(self):
        return self.position_ring[self.relative_board.index('A')]

    @ring_setting.setter
    def ring_setting(self, setting):
        """Sets rotor indicator offset relative to the internal wiring"""
        self._generic_setter("Invalid ring setting \"%s\"!", lambda: getattr(self, 'ring_setting'),
                             setting, lambda: self._change_board_offset('relative_board'))


class UKW_D:
    """Could be used in 3 rotor enigma versions, mostly used in EnigmaM4
    ( replacing the thin reflector and extra rotor! )"""
    def __init__(self, pairs=tuple()):
        self._pairs = WiredPairs('BO')
        self.alphabet =   "ACDEFGHIJKLMNPQRSTUVWXYZ"
        self.index_ring = "AZXWVUTSRQPONMLKIHGFEDCB"
        self.wiring_pairs = pairs

    @property
    def wiring_pairs(self):
        return self._pairs.pairs

    @wiring_pairs.setter
    def wiring_pairs(self, pairs):
        assert len(pairs) == 12, "Invalid number of pairs, " \
                                 "only number of pairs possible is 12!"
        new_pairs = []
        for pair in pairs:
            curr_pair = ''
            for letter in pair:
                curr_pair += self.alphabet[self.index_ring.index(letter)]
            new_pairs.append(curr_pair)
        new_pairs.append('BO')
        self._pairs.pairs = new_pairs

    def reflect(self, letter):
        return self._pairs.pairs_route(letter)


class Luckenfuller(Rotor):
    def __init__(self, label, back_board, turnover):
        Rotor.__init__(self, label, back_board, turnover)

    @property
    def turnover(self):
        return self._turnover

    @Rotor.turnover.setter
    def turnover(self, turnover):
        self._turnover = turnover


__all__ = ['EnigmaFactory', 'RotorFactory', 'Enigma1', 'EnigmaM3', 'EnigmaM4',
           'Reflector', 'Stator', 'Rotor', 'UKW_D', 'Uhr', 'Luckenfuller']
