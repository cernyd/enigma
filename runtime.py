from unit_tests.unit_tests import TestEnigma, unittest
from gui import Root


# Main unittest before running, could warn about potential flaws
# unittest.main(exit=False)


if __name__ == '__main__':
    root = Root()
    root.mainloop()
