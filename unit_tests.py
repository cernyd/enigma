import unittest
from functools import wraps

from enigma import Enigma


def reset_subject(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.reset_subject()
        func(self, *args, **kwargs)

    return wrapper


@reset_subject
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

    def test_settings(self):
        """Tests if all settings are assigned correctly"""
        self.reset_subject()

        # Test data
        ring_settings = ['C', 'B', 'A']
        rotors = ['III', 'I', 'II']
        positions = ['A', 'B', 'C']
        reflector = 'UKW-A'

        self.subject.positions = positions
        self.assertEqual(self.subject.positions, positions,
                         'Positions assigned in wrong order!')

        self.subject.reflector = reflector
        self.assertEqual(self.subject.reflector_label, reflector,
                         'Invalid rotor assigned!')

        self.subject.ring_settings = ring_settings
        self.assertEqual(self.subject.ring_settings, ring_settings,
                         'Invalid ring settings assigned!')

        self.subject.rotors = rotors
        self.assertEqual(self.subject.rotor_labels, rotors,
                         'Invalid rotor order assigned!')

    def test_cfg_io(self):
        """Tests if rotor data is dumped and loaded correctly"""

    def test_enigma_cfg_io(self):
        """Tests if enigma data is dumped and loaded correctly"""
        pass
