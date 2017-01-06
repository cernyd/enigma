from gui_components.root_gui import Root
from unit_tests.unit_tests import TestEnigma, unittest
from enigma_components.enigma import TkEnigma

# Main unittest before running, could warn about potential flaws
# unittest.main(exit=False)

test = TkEnigma(object(),'UKW-C' ,['I', 'II', 'III'])
# test.reflector = 'UKW-A'

# if __name__ == '__main__':
#     root = Root()
#     root.mainloop()
