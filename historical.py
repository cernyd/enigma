class Enigma1:
    """
    Historically accurate Enigma 1 rotor wiring
    UKW - Reflector
    ETW - Stationary router
    """

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
