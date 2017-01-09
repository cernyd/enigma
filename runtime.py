from unit_tests.unit_tests import TestEnigma, unittest
from gui import Root
from cfg_handler import Config


# Main unittest before running, could warn about potential flaws
unittest.main(exit=False)


if __name__ == '__main__':
    config = Config(['config.xml'])
    font = config.get_data(['globals', 'font']).keys()
    bg = config.get_data(['globals', 'bg'])['color']
    root_config = Config(['enigma', 'historical_data.xml'])
    root = Root(root_config, bg, font)
    root.mainloop()
