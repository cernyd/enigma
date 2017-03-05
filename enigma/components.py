from string import ascii_uppercase as alphabet
from itertools import permutations, chain
from cfg_handler import Config
from functools import wraps
import unittest
from tkinter import messagebox

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
        buffer = self.cfg.find('default_cfg')
        self.subject = self.enigma_factory.produce('EnigmaM3')

    def test_encrypt_decrypt(self):
        """Tests if encryption and decryption are working properly"""
        buffer = self.cfg.find('test_encrypt_decrypt')
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
        rotors = self.cfg.find('test_rotors')['rotors']
        self.subject.rotors = rotors
        self.assertEqual(self.subject.rotor_labels, rotors,
                         'Invalid rotor order assigned!')

    def test_positions(self):
        """Tests if rotor positions are set properly"""
        self.reset_subject()
        positions = self.cfg.find('test_positions')['positions']
        self.subject.positions = positions
        self.assertEqual(self.subject.positions, positions,
                         'Positions assigned in wrong order!')
        with self.assertRaises(AssertionError):
            self.subject.positions = 14651, 'garbage', -15

    def test_reflector(self):
        """Tests if the reflector is set properly"""
        self.reset_subject()
        reflector = self.cfg.find('test_reflector')['reflector']
        self.subject.reflector = reflector
        self.assertEqual(self.subject.reflector_label, reflector,
                         'Invalid rotor assigned!')
        with self.assertRaises(AssertionError):
            self.subject.reflector = 'garbage_input'

    def test_ring_settings(self):
        """Tests if ring settings are set properly"""
        self.reset_subject()
        ring_settings = self.cfg.find('test_ring_settings')['ring_settings']
        self.subject.ring_settings = ring_settings
        self.assertEqual(self.subject.ring_settings, ring_settings,
                         'Invalid ring settings assigned!')
        with self.assertRaises(AssertionError):
            self.subject.ring_settings = [12, 'garbage_input', 798715]

    def test_plugboard(self):
        """Checks if plugboard pairs are set propertly"""
        self.reset_subject()
        plug_pairs = self.cfg.find('test_plugboard')['pairs']
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

def join_list(lst):
    return list(chain.from_iterable(lst))


def are_unique(pairs, error_msg='Contains duplicate pairs!'):
    value_list = join_list(pairs)
    assert len(value_list) == len(set(value_list)), error_msg


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

        are_unique(pairs, 'A letter can only be wired once!')

        self._pairs = pairs

    def pairs_route(self, letter):
        neighbour = []
        for pair in self._pairs:
            if letter in pair:
                neighbour.extend(pair)
                neighbour.remove(letter)
                return neighbour[0]
        return letter  # If no connection found


# PLUGBOARD

class Plugboard:
    """Standard and Uhr pairs can be set"""
    def __init__(self, normal_pairs=tuple(), uhr_pairs=tuple()):
        self._wired_pairs = WiredPairs()  # Self steckered, no scrambling
        self._uhr = Uhr()  # Uhr steckered, always 10 pairs
        # Pairs are stored additionally for easier searching, WILL REMOVE LATER
        self.set_pairs(normal_pairs, uhr_pairs)

    def set_pairs(self, normal_pairs=tuple(), uhr_pairs=tuple()):
        """Allows to set up to 13 normal pairs or 10 Uhr pairs + up to 3 normal
        pairs"""
        are_unique(normal_pairs + uhr_pairs), "A letter can only be wired once!"
        if uhr_pairs:
            self._uhr.pairs = uhr_pairs
        self._wired_pairs.pairs = normal_pairs

    def get_pairs(self):
        """Returns list of all combined connected pairs"""
        return {'uhr_pairs': self._uhr.simple_pairs, 'normal_pairs': self._wired_pairs.pairs}

    def route(self, letter):
        """Routes letter either with Uhr or with normal pairs"""
        if letter in join_list(self._uhr.simple_pairs):
            return self._uhr.route(letter)
        else:
            return self._wired_pairs.pairs_route(letter)

    @property
    def uhr_connected(self):
        return len(self._uhr.simple_pairs) != 0

    @property
    def uhr_position(self):
        return self._uhr.position

    @uhr_position.setter
    def uhr_position(self, position):
        self._uhr.position = position


# ENIGMA MODELS

class EnigmaFactory:
    """Factory for producing enigma machines ( initialised more simply by
    choosing defaults from available config )"""
    def __init__(self, cfg_path):
        self._rotor_factory = RotorFactory(cfg_path)

    @staticmethod
    def _get_model_class(model):
        try:
            return globals()[model]
        except KeyError:
            raise KeyError(f"No enigma model found for \"{model}\"!")

    def _get_model_data(self, enigma_model, reflector=None, rotors=None, stator=None):
        model = enigma_model.__name__
        model_data = self._rotor_factory.model_data(model)

        # This block generates default data if specific preferences were not specified
        if not reflector:
            reflector = model_data['reflectors'][0]
        if not rotors:
            rotors = model_data['rotors'][:enigma_model.rotor_count]
        if not stator:
            stator = model_data['stators'][0]

        return self._rotor_factory.produce(model, 'reflector', reflector), \
               [self._rotor_factory.produce(model, 'rotor', label) for label in rotors], \
               self._rotor_factory.produce(model, 'stator', stator), model_data


    def produce(self, model, reflector=None, rotors=None, stator=None, master=None):
        """Produces an enigma machine given a specific model ( must be available
        in the specified cfg_path )"""
        ModelClass = self._get_model_class(model)
        data = self._get_model_data(ModelClass, reflector, rotors, stator)

        if master:
            class TkEnigma(ModelClass):
                """Enigma adjusted for Tk rotor lock,
                    ignore the property signatures please..."""
                def __init__(self, master, rotor_factory, *data):
                    self._rotor_factory = rotor_factory
                    ModelClass.__init__(self, *data)
                    self.master = master

                def _rotate_primary(self, places=1):
                    if not self.master.rotor_lock:
                        ModelClass.step_primary(self, places)

                @ModelClass.reflector.setter
                def reflector(self, reflector):
                    try:
                        if type(reflector) == str:
                            ModelClass.reflector.fset(self, self._rotor_factory.produce(model, 'reflector', reflector))
                        else:
                            ModelClass.reflector.fset(self, reflector)
                    except AttributeError as err:
                        messagebox.showwarning('Invalid reflector',
                                               'Invalid reflector,'
                                               ' please try '
                                               'again...')

                @ModelClass.rotors.setter
                def rotors(self, rotors):
                    """Adds a visual error feedback ( used only in the tk implementation"""
                    try:
                        if type(rotors[0]) == str:
                            ModelClass.rotors.fset(self, [self._rotor_factory.produce(model, 'rotor', label) for label in rotors])
                        else:
                            ModelClass.rotors.fset(self, rotors)
                    except AttributeError as err:
                        messagebox.showwarning('Invalid rotor',
                                               'Some of rotors are not \n'
                                               'valid, please try again...')

                @property
                def all_rotor_labels(self):
                    return self.rotor_factory['rotors']

                @property
                def all_reflector_labels(self):
                    return self.factory_data['reflectors']

                @property
                def labels(self):
                    return self.factory_data['labels']

                @property
                def layout(self):
                    return self.factory_data['layout']

            return TkEnigma(master, self._rotor_factory, *data)
        else:
            return ModelClass(*data)


class Enigma:
    """Base for all enigma objects, has no plugboard, default rotor count for
    all enigma machines is 3."""
    rotor_count = 3
    plugboard = False

    def __init__(self, reflector, rotors, stator, factory_data=None):
        self._stator = stator
        self._rotors = None
        self.rotors = rotors
        self._reflector = None
        self.reflector = reflector

        self.factory_data = factory_data  # All available components

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
    plugboard = True

    def __init__(self, reflector, rotors, stator, factory_data, normal_pairs=tuple(), uhr_pairs=tuple()):
        Enigma.__init__(self, reflector, rotors, stator, factory_data)
        self._plugboard = Plugboard(normal_pairs, uhr_pairs)

    @property
    def plugboard(self):
        """Plugboard routing pairs"""
        return self._plugboard.get_pairs()

    @plugboard.setter
    def plugboard(self, normal_pairs=tuple(), uhr_pairs=tuple()):
        self._plugboard.set_pairs(normal_pairs, uhr_pairs)

    def button_press(self, letter):
        """Wraps the base enigma routing with plugboard"""
        output = self._plugboard.route(letter)
        output = Enigma.button_press(self, output)
        return self._plugboard.route(output)

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

    def model_data(self, model):
        """Returns all available rotor labels for the selected enigma model"""
        model_data = {}

        for row in self.cfg.find('layout', 'SUBATTRS'):
            if not model_data.get('layout', None):
                model_data['layout'] = [row['values']]
            else:
                model_data['layout'].append(row['values'])

        # DUPLICATE KNOWLEDGE!
        for row in self.cfg.find('labels', 'SUBATTRS'):
            if not model_data.get('labels', None):
                model_data['labels'] = row['values']
            else:
                model_data['labels'].extend(row['values'])

        self.cfg.focus_buffer(self._base_path.format(model=model))
        for item in ['rotors', 'reflectors', 'stators']:
            model_data[item] = [rotor['label'] for rotor in self.cfg.find(item, 'SUBATTRS')]

        return model_data

    def produce(self, model, rotor_type, label):
        """Creates and returns new object based on input"""
        self.cfg.focus_buffer(self._base_path.format(model=model))
        cfg = self.cfg.iter_find(rotor_type)

        match = False
        for item in cfg:
            if item['label'] == label:
                cfg = item
                match = True
                break

        err_msg = f"No configuration found for label \"{label}\"!"
        assert match, err_msg
        if rotor_type == 'rotor':
            return Rotor(**cfg)
        elif rotor_type == 'reflector':
            return Reflector(**cfg)
        elif rotor_type == 'stator':
            return Stator(**cfg)


class _RotorBase:
    """Base class for Rotors and Reflectors"""
    def __init__(self, label, back_board, valid_cfg=tuple()):
        """All parameters except should be passed in **config, valid_cfg is a
        tuple of additional configuration data for config loading and dumping"""
        self.valid_cfg = ['back_board', 'label']
        self.valid_cfg.extend(valid_cfg)

        self.back_board = back_board  # Defines internal wiring
        self.label = label

    def _check_input(func):
        """Checks if the rotor is given correct input ( a single letter for the
        alphabet )"""
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
    @_RotorBase._check_input
    def reflect(self, letter):
        """Reflects letter back"""
        return self._route_forward(letter)


class Stator(_RotorBase):
    @_RotorBase._check_input
    def forward(self, letter):
        """Routes letter from front to back"""
        return self._route_forward(letter)

    @_RotorBase._check_input
    def backward(self, letter):
        """Routes letter from back to front"""
        return alphabet[self.back_board.index(letter)]


class Rotor(Stator, _Rotatable):
    """Inherited from RotorBase, adds rotation and ring setting functionality"""
    def __init__(self, label,  back_board, turnover=''):
        Stator.__init__(self, label, back_board,
                            valid_cfg=('position_ring', '_Rotor_turnover', 'relative_board'))
        self._turnover = turnover  # Letter shown on turnover position

        # position_ring = position currently shown in the position window,
        # relative_board = used in the actual wiring ( internal, between
        # position rings )
        self.position_ring, self.relative_board = [alphabet] * 2

    def _compensate(func):
        """Converts input to relative input and
        relative output to absolute output, does some assertions too."""
        @wraps(func)
        def wrapper(self, letter):
            relative_input = self.relative_board[alphabet.index(letter)]
            return alphabet[
                self.relative_board.index(func(self, relative_input))]
        return wrapper

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


# HISTORICAL ENIGMA PECULIARITIES

class Luckenfuller(Rotor):
    """Rotor with adjustable turnover notches."""
    def __init__(self, label, back_board, turnover):
        Rotor.__init__(self, label, back_board, turnover)

    @Rotor.turnover.setter
    def turnover(self, turnover):
        self._turnover = turnover


class UKW_D:
    """Could be used in 3 rotor enigma versions, mostly used in EnigmaM4
    ( replacing the thin reflector and extra rotor! ). UKW-D is a field
    rewirable Enigma machine reflector."""
    def __init__(self, pairs=tuple()):
        self._pairs = WiredPairs('BO')  # BO pair is static!
        self.alphabet =  "ACDEFGHIJKLMNPQRSTUVWXYZ"
        self.index_ring = "AZXWVUTSRQPONMLKIHGFEDCB"
        self.wiring_pairs = pairs

    @property
    def wiring_pairs(self):
        """Wiring pairs of the reflector"""
        return self._pairs.pairs

    @wiring_pairs.setter
    def wiring_pairs(self, pairs):
        """Sets up wiring pairs, BO is static!"""
        assert len(pairs) == 12, "Invalid number of pairs, " \
                                 "only number of pairs possible is 12!"

        all_letters = join_list(pairs)
        assert 'B' not in all_letters and 'O' not in all_letters, \
            "The 'BO' pair is hardwired and can not be rewired"
        pairs.append('BO')
        self._pairs.pairs = pairs

    def reflect(self, letter):
        return self._pairs.pairs_route(letter)


class Uhr(_Rotatable):
    """Uhr is an enigma machine extension, allows the plugboard to be scrambled
    based on a key, every 4th position starting with 00 is reciprocal, maximum
    position is 40. All other positions are not reciprocal ( encryption is not
    directly reversible: A > B, B > X ( not A! )."""
    def __init__(self, pairs=''):
        """On position 00, all bx cables are connected to corresponding ax
        cables. Position 00 is reciprocal and allows communication with non-uhr
        users."""
        self.back_board = [26, 11, 24, 21, 2, 31, 0, 25, 30, 39, 28, 13, 22, 35,
                          20, 37, 6, 23, 4, 33, 34, 19, 32, 9, 18, 7, 16, 17,
                          10, 3, 8, 1, 38, 27, 36, 29, 14, 15, 12, 5]
        self.relative_board = tuple(range(40))
        # Relative and indicator boards are the same because Uhr did not have turnovers

        # Number pairs stand for ( SEND, RECEIVE )
        # WARNING - These positions are absolute, only the wiring disk has offset
        self._black_red_plug_pairs = {'1a': (0, 2), '1b': (4, 6),
                                      '2a': (4, 6), '2b': (16, 18),
                                      '3a': (8, 10), '3b': (28, 30),
                                      '4a': (12, 14), '4b': (36, 38),
                                      '5a': (16, 18), '5b': (24, 26),
                                      '6a': (20, 22), '6b': (12, 14),
                                      '7a': (24, 26), '7b': (0, 2),
                                      '8a': (28, 30), '8b': (8, 10),
                                      '9a': (32, 34), '9b': (20, 22),
                                      '10a': (36, 38), '10b': (32, 34)}

        self._pairs = {}
        self._simple_pairs = []  # THIS IS JUST A VIEW, REFACTOR ASAP
        self.pairs = pairs

    @property
    def simple_pairs(self):
        return self._simple_pairs

    @property
    def pairs(self):
        return self._pairs

    @pairs.setter
    def pairs(self, pairs):
        """Uhr has exacly 10 pairs of wires because it was the standard number of
        plugboard connections during the war ( mathematically optimal number,
        increases the possible pair number greatly in combinatorics )
        1 pair: 325
        2 pairs: 44.850
        3 pairs: 3,453,450
        4 pairs: 164,038,875
        5 pairs: 5,019,589,575
        6 pairs: 100,391,791,500
        7 pairs: 1,305,093,289,500
        8 pairs: 10,767.019,638,375
        9 pairs: 58,835.098,191,875
        10 pairs: 150,738,274,937,250
        11 pairs: 205,552,193,096,250
        12 pairs: 102,776,096,548,125
        13 pairs: 7,905,853,580,625"""

        if len(pairs) > 0:
            assert (len(pairs) == 10), "All 10 pairs must be wired, otherwise " \
                                       "electrical signal could be lost during " \
                                       "non-reciprocal substitution."
            are_unique(pairs, 'Letters in Uhr pairs can only be wired once!')
            # Connects letter pairs to a corresponding aX - bX pair
            for pair, index in zip(pairs, range(1, 11)):
                for letter, socket_id in zip(pair, 'ab'):
                    full_socket_id = str(index) + socket_id
                    socket_data = self._black_red_plug_pairs[full_socket_id]
                    self.pairs[letter] = (full_socket_id, socket_data)

            self._simple_pairs = pairs
        else:
            self._simple_pairs = []
            self._pairs = {}

    @property
    def position(self):
        return self.relative_board[0]

    @position.setter
    def position(self, position):
        if position not in range(40):
            raise AssertionError(f'Invalid Uhr position of "{position}"')
        while self.relative_board[0] != position:
            self._change_board_offset('relative_board', 1)
            self._change_board_offset('back_board', 1)

    def _compensate(func):
        """Compensates for the rotor rotation"""
        @wraps(func)
        def wrapper(self, absolute_input):
            relative_input = self.relative_board[absolute_input]  # Correct
            relative_output = func(self, relative_input)
            absolute_output = range(40)[self.relative_board.index(relative_output)]
            return absolute_output
        return wrapper

    @_compensate
    def _route_forward(self, position):
        """Routes letter from A board to B board, absolute! > does not
        compensate for disc offset"""
        return self.relative_board[self.back_board.index(position)]

    @_compensate
    def _route_backward(self, position):
        """Routes letter from B board to A board, absolute! > does not
        compensate for disc offset"""
        return self.back_board[self.relative_board.index(position)]

    def find_letter(self, board_letter, target):
        """Finds letter based on the target index and target board"""
        for pair in self._pairs.items():
            if board_letter in pair[1][0]:
                if target == pair[1][1][1]:
                    return pair[0]

    def route(self, letter):
        """Routes letter trough the Uhr disk."""
        letter_data = self._pairs[letter.upper()]
        output_pin_index = letter_data[1][0]

        if 'a' in letter_data[0]:
            letter = self.find_letter('b', self._route_forward(output_pin_index))
        else:
            letter = self.find_letter('a', self._route_backward(output_pin_index))

        assert letter, "No letter found!"
        return letter


__all__ = ['EnigmaFactory', 'RotorFactory', 'Enigma1', 'EnigmaM3', 'EnigmaM4',
           'Reflector', 'Stator', 'Rotor', 'UKW_D', 'Uhr', 'Luckenfuller']
