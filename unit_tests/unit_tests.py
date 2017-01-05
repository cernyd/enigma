import unittest
import xml.etree.ElementTree as ET
from itertools import permutations
from os import path

from enigma_components.enigma import Enigma


def cfg_interface(category):
    tree = ET.parse(path.join('unit_tests', 'test_cfg.xml'))
    if type(category) == 'class':
        category = category.__name__
    data = tree.getroot().find(category).attrib

    if len(data) == 1:
        return data.keys()[0].split()
    else:
        return data


class TestEnigma(unittest.TestCase):
    """Used to test if enigma class behaves like the real life counterpart"""
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.subject: Enigma
        print('Got here')
        self.reset_subject()

    def reset_subject(self):
        buffer = cfg_interface('default_cfg')
        self.subject = Enigma(buffer['reflector'], buffer['rotors'].split())

    def test_encrypt_decrypt(self):
        """Tests if encryption and decryption are working properly"""
        buffer = cfg_interface(self)
        for test in permutations(['encrypted', 'decrypted']):
            self.reset_subject()
            output = ''
            for letter in buffer[test[0]]:
                output += self.subject.button_press(letter)
            self.assertEqual(output, buffer[test[0]], f'Failed to '
                                                             f'{test[1][:-2]}!')

    def test_rotors(self):
        """Tests if rotors are assigned properly"""
        self.reset_subject()
        rotors = cfg_interface(self)
        self.subject.rotors = rotors
        self.assertEqual(self.subject.rotor_labels, rotors,
                         'Invalid rotor order assigned!')

    def test_positions(self):
        """Tests if rotor positions are set properly"""
        self.reset_subject()
        positions = cfg_interface(self)
        self.subject.positions = positions
        self.assertEqual(self.subject.positions, positions,
                         'Positions assigned in wrong order!')

    def test_reflector(self):
        """Tests if the reflector is set properly"""
        self.reset_subject()
        reflector = cfg_interface(self)
        self.subject.reflector = reflector
        self.assertEqual(self.subject.reflector_label, reflector,
                         'Invalid rotor assigned!')

    def test_ring_settings(self):
        """Tests if ring settings are set properly"""
        self.reset_subject()
        ring_settings = cfg_interface(self)
        self.subject.ring_settings = ring_settings
        self.assertEqual(self.subject.ring_settings, ring_settings,
                         'Invalid ring settings assigned!')

    def test_plugboard(self):
        """Checks if plugboard pairs are set propertly"""
        self.reset_subject()
        plug_pairs = cfg_interface(self)
        self.subject.plugboard = plug_pairs
        self.assertEqual(self.subject.plugboard, plug_pairs, 'Invalid plugboard'
                                                             ' pairs assigned!')

    def test_cfg_io(self):
        """Tests if rotor data is dumped and loaded correctly"""

    def test_enigma_cfg_io(self):
        """Tests if enigma data is dumped and loaded correctly"""
