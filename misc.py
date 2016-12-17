from os import path
from collections import OrderedDict
from string import ascii_uppercase
# from rotor import Rotor, Reflector


# CONFUSED AS TO WHAT THIS MISC FILE DOES


alphabet = ascii_uppercase


labels = ['A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06',
              'G-07', 'H-08', 'I-09', 'J-10', 'K-11', 'L-12',
              'M-13', 'N-14', 'O-15', 'P-16', 'Q-17', 'R-18',
              'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24',
              'Y-25', 'Z-26']


layout = [[16, 22, 4, 17, 19, 25, 20, 8, 14],
          [0, 18, 3, 5, 6, 7, 9, 10],
          [15, 24, 23, 2, 21, 1, 13, 12, 11]]


def get_label(wiring):
    """Finds the rotor label corresponding to the input wiring"""
    for key, value in dict(**Enigma1.rotors, **Enigma1.reflectors).items():
        if value[0] == wiring:
            return key
        elif value == wiring:
            return key


def get_icon(icon):
    """Gets icon path from the icon folder"""
    return path.join('icons', icon)


class Enigma1:
    """Historically accurate Enigma 1 rotor and reflector wiring, useful position
    labels are available too"""
    rotors = OrderedDict((('I', ['EKMFLGDQVZNTOWYHXUSPAIBRCJ', 16]),
                         ('II', ['AJDKSIRUXBLHWTMCQGZNPYFVOE', 12]),
                         ('III', ['BDFHJLCPRTXVZNYEIWGAKMUSQO', 3]),
                         ('IV', ['ESOVPZJAYQUIRHXLNFTGKDCMWB', 17]),
                         ('V', ['VZBRGITYUPSDNHLXAWMJQOFECK', 7])))

    reflectors = OrderedDict((('UKW-A', 'EJMZALYXVBWFCRQUONTSPIKHGD'),
                             ('UKW-B', 'YRUHQSLDPXNGOKMIEBFZCWVJAT'),
                             ('UKW-C', 'FVPJIAOYEDRZXWGCTKUQSBNMHL')))


class RotorFactory:
    factory_data = {'Enigma1': {'rotor': [('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 16),
                                          ('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 12),
                                          ('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 3),
                                          ('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 17),
                                          ('I', 'VZBRGITYUPSDNHLXAWMJQOFECK', 7)],
                               'reflector': [('UKW-A', 'EJMZALYXVBWFCRQUONTSPIKHGD'),
                                              ('UKW-B', 'YRUHQSLDPXNGOKMIEBFZCWVJAT'),
                                              ('UKW-C', 'FVPJIAOYEDRZXWGCTKUQSBNMHL')]}}

    def __new__(cls):
        raise NotImplementedError('This class was not intended for instantiation!')

    @classmethod
    def produce(cls, model, rotor_type, label):
        for item in cls.factory_data[model][rotor_type]:
            if item[0] == label:
                cfg = cls.create_cfg(*item)
                break

        if rotor_type == 'rotor':
            return  # Rotor()
        elif rotor_type == 'reflector':
            return  # Reflector()

    @classmethod
    def create_cfg(cls, label, back_board, turnover=None):
        """Creates a configuration dictionary"""
        cfg = dict(label=label, back_board=back_board)
        if turnover:
            cfg.update(turnover=turnover)
        return cfg


def baseinit(self):
    # Load smoothness upgrade
    self.attributes("-alpha", 0.0)
    self.after(0, self.attributes, "-alpha", 1.0)
    self.resizable(False, False)
    self.grab_set()
