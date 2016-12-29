from root_gui import Root

if __name__ == '__main__':
    root = Root()
    root.mainloop()


# ----------------------------------- Debug part ------------------------------

# test = Enigma('UKW-B', ['I', 'II', 'III'])

# test.ring_settings = 'A', 'B', 'C'
# try:
#     while True:
#         system('cls')
#         data = [test.rotor_labels[1:], test.positions, test.rotor_turnovers,
#                 test.ring_settings]
#         print('SLOW - MEDIUM - FAST')
#         for item in data:
#             print('{} - {} - {}'.format(*item))
#         input()
#         test.rotate_primary()
# except Exception as err:
#     input(err)

# from rotor_factory import RotorFactory
# test = RotorFactory.produce('Enigma1', 'rotor', 'I')
# test.set_ring_setting('F')
# test.set_position('Y')
# input()
# while True:
#     system('cls')
#     print('Output > ', test.forward('A'))
#     # print('Position ring  > ', test.position_ring)
#     # print('Relative board > ', list(test.relative_board))
#     input()
#     test.rotate()

# Rotor I, ring setting 6, pos 25, input A, output W!

# -----------------------------------------------------------------------------
