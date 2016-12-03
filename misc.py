from os import path

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_label(wiring):
    """Finds the rotor label corresponding to the input wiring"""
    for key, value in Enigma1.rotors.items():
        if value[0] == wiring:
            return key
        elif value == wiring:
            return key


def unique_pairs(pairs):
    return_pairs = []
    for pair in pairs:
        if pair not in return_pairs and list(reversed(pair)) not in return_pairs:
            if all(pair):
                return_pairs.append(pair)
    return return_pairs


def get_icon(icon):
    """Gets icon path from the icon folder"""
    return path.join('icons', icon)


class Enigma1:
    """Historically accurate Enigma 1 rotor and reflector wiring, useful position
    labels are available too"""
    rotors = {
              'I': ['EKMFLGDQVZNTOWYHXUSPAIBRCJ', 16],
              'II': ['AJDKSIRUXBLHWTMCQGZNPYFVOE', 12],
              'III': ['BDFHJLCPRTXVZNYEIWGAKMUSQO', 3],
              'IV': ['ESOVPZJAYQUIRHXLNFTGKDCMWB', 17],
              'V': ['VZBRGITYUPSDNHLXAWMJQOFECK', 7],
              'UKW-A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
              'UKW-B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
              'UKW-C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
              }

    labels =['A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06',
                               'G-07', 'H-08', 'I-09', 'J-10','K-11', 'L-12',
                               'M-13', 'N-14', 'O-15', 'P-16', 'Q-17', 'R-18',
                               'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24',
                               'Y-25','Z-26']
