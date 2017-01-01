import unittest
from itertools import permutations

from enigma_components.enigma import Enigma


class TestEnigma(unittest.TestCase):
    """Used to test if enigma class behaves like the real life counterpart"""
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.default_cfg = 'UKW-B', ['I', 'II', 'III']
        self.subject = Enigma(*self.default_cfg)
        self.encrypted = 'FQGAHWLMJAMTJAANUNPDY'
        self.decrypted = 'ENIGMAUNITTESTMESSAGE'

    def reset_subject(self):
        self.subject = Enigma(*self.default_cfg)

    def test_encrypt_decrypt(self):
        """Tests if encryption and decryption are working properly"""
        for test in permutations(['encrypted', 'decrypted']):
            self.reset_subject()
            output = ''
            for letter in getattr(self, test[0]):
                output += self.subject.button_press(letter)
            self.assertEqual(output, getattr(self, test[1]), f'Failed to '
                                                             f'{test[1][:-2]}!')

    def test_rotors(self):
        """Tests if rotors are assigned properly"""
        self.reset_subject()
        rotors = ['III', 'I', 'II']
        self.subject.rotors = rotors
        self.assertEqual(self.subject.rotor_labels, rotors,
                         'Invalid rotor order assigned!')

    def test_positions(self):
        """Tests if rotor positions are set properly"""
        self.reset_subject()
        positions = ['A', 'B', 'C']
        self.subject.positions = positions
        self.assertEqual(self.subject.positions, positions,
                         'Positions assigned in wrong order!')

    def test_reflector(self):
        """Tests if the reflector is set properly"""
        self.reset_subject()
        reflector = 'UKW-A'
        self.subject.reflector = reflector
        self.assertEqual(self.subject.reflector_label, reflector,
                         'Invalid rotor assigned!')

    def test_ring_settings(self):
        """Tests if ring settings are set properly"""
        self.reset_subject()
        ring_settings = ['C', 'B', 'A']
        self.subject.ring_settings = ring_settings
        self.assertEqual(self.subject.ring_settings, ring_settings,
                         'Invalid ring settings assigned!')

    def test_plugboard(self):
        """Checks if plugboard pairs are set propertly"""
        self.reset_subject()
        plug_pairs = [['A', 'Q'], ['X', 'P'], ['F', 'G'], ['D', 'R']]
        self.subject.plugboard = plug_pairs
        self.assertEqual(self.subject.plugboard, plug_pairs, 'Invalid plugboard'
                                                             ' pairs assigned!')

    def test_cfg_io(self):
        """Tests if rotor data is dumped and loaded correctly"""

    def test_enigma_cfg_io(self):
        """Tests if enigma data is dumped and loaded correctly"""
