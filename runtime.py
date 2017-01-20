# from cfg_handler import Config
# from gui import Root
# from unit_tests import TestEnigma, unittest
from enigma.components import *


# config = Config('config.xml')
# config.focus_buffer('globals')
# font = list(config.get_data('font').values())
# bg = config.get_data('bg')['color']
# enigma_cfg = config.get_data('enigma_defaults')
# root = Root(enigma_cfg, Config('config.xml'), bg, font)
#
#
# # Main unittest before running, could warn about potential flaws
# if config.get_data(['unit_tests'])['startup_test'] == "True":
#     TestEnigma.model = enigma_cfg['model']
#     TestEnigma.cfg_path = ['config.xml']
#     unittest.main(exit=False, verbosity=2)
#
#
# if __name__ == '__main__':
#     root.mainloop()

# while True:
#     print()
#     factory = RotorFactory(['enigma', 'historical_data.xml'], input('Enter enigma model: '))
#     reflector = factory.produce('reflectors', input('Enter reflector: '))
#
#     rotors=[]
#     for label in input('Enter rotors: ').split():
#         rotors.append(factory.produce('rotors', label))
#
#     stator = factory.produce('stators', input('Enter stator: '))
#     myEnigma = EnigmaM4(input('Enter plug pairs: ').split(), reflector, rotors, stator)
#     myEnigma.ring_settings = input('Enter ring settings: ').split()
#     myEnigma.positions = input('Enter positions: ').split()
#     for letter in input('Enter message: ').replace(' ', ''):
#         print(myEnigma.button_press(letter), end='')
