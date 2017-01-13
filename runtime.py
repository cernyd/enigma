from unit_tests.unit_tests import TestEnigma, unittest
from gui import Root
from cfg_handler import Config


config = Config(['config.xml'])
font = list(config.get_data(['globals', 'font']).values())
bg = config.get_data(['globals', 'bg'])['color']
default_enigma = config.get_data(['globals', 'enigma_defaults'])['model']
root = Root(default_enigma, Config(['enigma', 'historical_data.xml']), bg, font)


# Main unittest before running, could warn about potential flaws
if config.get_data(['globals', 'unit_tests'])['startup_test'] == "True":
    TestEnigma.model = default_enigma
    unittest.main(exit=False, verbosity=2)


if __name__ == '__main__':

    root.mainloop()
