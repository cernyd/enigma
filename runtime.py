from gui_components.root_gui import Root
from unit_tests import unittest

# Main unittest before running, could warn about potential flaws
unittest.main(exit=False)


if __name__ == '__main__':
    root = Root()
    root.mainloop()
