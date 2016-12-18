from os import path
from collections import OrderedDict
from string import ascii_uppercase
# from rotor import Rotor, Reflector


# CONFUSED AS TO WHAT THIS MISC FILE DOES


alphabet = ascii_uppercase





def get_icon(icon):
    """Gets icon path from the icon folder"""
    return path.join('icons', icon)


def baseinit(self):
    # Load smoothness upgrade
    self.attributes("-alpha", 0.0)
    self.after(0, self.attributes, "-alpha", 1.0)
    self.resizable(False, False)
    self.grab_set()
