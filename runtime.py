from root_gui import Root

"""
if __name__ == '__main__':
    root = Root()
    root.mainloop()
"""

# ----------------------------------- Debug part ------------------------------

from os import system

# from enigma import Enigma
# test = Enigma('UKW-B', ['I', 'II', 'III'])
# test.ring_settings = 1,2,3
# try:
#     while True:
#         system('cls')
#         data = [test.rotor_labels[1:], test.positions, test.rotor_turnovers[1:],
#                 test.ring_settings]
#         print('SLOW - MEDIUM - FAST')
#         for item in data:
#             print('{} - {} - {}'.format(*item))
#         input()
#         test.rotate_primary()
# except Exception as err:
#     input(err)

from rotor_factory import RotorFactory
test = RotorFactory.produce('Enigma1', 'rotor', 'I')
test.set_ring_setting(2)
while True:
    # system('cls')
    print('Output > ', test.forward('A'))
    # print('Ring setting > ', test.get_ring_setting())
    # print('Position ring  > ', test.position_ring)
    # print('Relative board > ', list(test.relative_board))
    input()
    test.rotate()

# -----------------------------------------------------------------------------
