from gui import Root
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

factory = EnigmaFactory(['enigma', 'historical_data.xml'])
print(factory.produce('Enigma1'))
