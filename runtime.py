from root_gui import Root


if __name__ == '__main__':
    root = Root()
    root.mainloop()


# Debug part
# from rotor_factory import RotorFactory
# test = RotorFactory.produce('Enigma1', 'rotor', 'I')
# test.set_ring_setting(2)
# print('Forwarded > ', test.forward('A'))
# print('Ring setting > ', test.get_ring_setting())
# print('Position ring  > ', test.position_ring)
# print('Relative board > ', list(test.relative_board))
