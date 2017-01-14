import unittest
from itertools import permutations
from enigma.components import Enigma
from cfg_handler import Config


class TestEnigma(unittest.TestCase):
    """Used to test if enigma class behaves like the real life counterpart"""
    model = 'Enigma1'
    cfg_path = []

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.cfg = Config(TestEnigma.cfg_path)
        self.cfg.focus_buffer('test_cfg')
        self.subject: Enigma
        self.reset_subject()

    def reset_subject(self):
        buffer = self.cfg.get_data('default_cfg')
        self.subject = Enigma(TestEnigma.model, buffer['reflector'], buffer['rotors'])

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

    def test_reflector(self):
        """Tests if the reflector is set properly"""
        self.reset_subject()
        reflector = self.cfg.get_data('test_reflector')['reflector']
        self.subject.reflector = reflector
        self.assertEqual(self.subject.reflector_label, reflector,
                         'Invalid rotor assigned!')

    def test_ring_settings(self):
        """Tests if ring settings are set properly"""
        self.reset_subject()
        ring_settings = self.cfg.get_data('test_ring_settings')['ring_settings']
        self.subject.ring_settings = ring_settings
        self.assertEqual(self.subject.ring_settings, ring_settings,
                         'Invalid ring settings assigned!')

    def test_plugboard(self):
        """Checks if plugboard pairs are set propertly"""
        self.reset_subject()
        plug_pairs = self.cfg.get_data('test_plugboard')['pairs']
        self.subject.plugboard = plug_pairs
        self.assertEqual(self.subject.plugboard, plug_pairs, 'Invalid plugboard'
                                                             ' pairs assigned!')

    # def test_cfg_io(self):
    #     """Tests if rotor data is dumped and loaded correctly"""
    #
    # def test_enigma_cfg_io(self):
    #     """Tests if enigma data is dumped and loaded correctly"""
