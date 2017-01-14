from cfg_handler import Config
from gui import Root
from unit_tests import TestEnigma, unittest

config = Config(['config.xml'])
font = list(config.get_data(['globals', 'font']).values())
bg = config.get_data(['globals', 'bg'])['color']
enigma_cfg = config.get_data(['globals', 'enigma_defaults'])
root = Root(enigma_cfg, Config(['enigma', 'historical_data.xml']), bg, font)


# Main unittest before running, could warn about potential flaws
if config.get_data(['globals', 'unit_tests'])['startup_test'] == "True":
    TestEnigma.model = enigma_cfg['model']
    TestEnigma.cfg_path = ['config.xml']
    unittest.main(exit=False, verbosity=2)


if __name__ == '__main__':
    root.mainloop()
