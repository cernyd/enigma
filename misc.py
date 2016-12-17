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


def get_icon(icon):
    """Gets icon path from the icon folder"""
    return path.join('icons', icon)


def baseinit(self):
    # Load smoothness upgrade
    self.attributes("-alpha", 0.0)
    self.after(0, self.attributes, "-alpha", 1.0)
    self.resizable(False, False)
    self.grab_set()
