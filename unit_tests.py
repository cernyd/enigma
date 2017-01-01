import unittest

from enigma_components.enigma import Enigma


class TestEnigma(unittest.TestCase):
    """Used to test if enigma class behaves like the real life counterpart"""
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.subject = Enigma('UKW-B', ['I', 'II', 'III'])

    def reset_subject(self):
        self.subject = Enigma('UKW-B', ['I', 'II', 'III'])

    def test_encryption(self):
        """Tests if encryption is done properly"""
        self.reset_subject()
        encrypted = ''
        for letter in 'ENIGMAUNITTESTMESSAGE':
            encrypted += self.subject.button_press(letter)
        self.assertEqual('FQGAHWLMJAMTJAANUNPDY', encrypted,
                         'Encryption test failed!')

    def test_decryption(self):
        """Tests if decryption is done properly"""
        self.reset_subject()
        decrypted = ''
        for letter in 'FQGAHWLMJAMTJAANUNPDY':
            decrypted += self.subject.button_press(letter)
        self.assertEqual('ENIGMAUNITTESTMESSAGE', decrypted,
                         'Decryption test failed!')

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
        self.subject.reflector = 'UKW-A'
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
