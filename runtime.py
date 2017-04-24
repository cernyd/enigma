#!/usr/bin/env python3

from enigma.components import TestEnigma, unittest
from data_handler import DataHandler
from gui import Root


data_handler = DataHandler()
root = Root(data_handler)


# Main unittest before running, could warn about potential flaws
# If this passes, enigma should be ready for accurate simulation
if data_handler.global_cfg.find(['unit_tests'])['startup_test'] == "True":
    TestEnigma.model = data_handler.enigma_cfg['model']
    TestEnigma.cfg_path = ['config.xml']
    unittest.main(exit=False, verbosity=1)


if __name__ == '__main__':
    root.mainloop()
