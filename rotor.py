from historical import Enigma1

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_label(wiring):
    for key, value in Enigma1.rotors.items():
        if value == wiring:
            return key


class Rotor:  # 26 letters in alphabet!
    def __init__(self, wiring, position=0, offset=0):
        self.label = get_label(wiring)
        self.front_board = alphabet
        self.back_board = wiring
        self.position = position
        self.offset = offset

    def forward(self, letter):
        return self.back_board[alphabet.index(letter)]

    def backward(self, letter):
        return alphabet[self.back_board.index(letter)]

    def set_offset(self, offset):
        offset = offset - self.offset
        self.back_board = self.back_board = self.back_board[
                                            offset:] + self.back_board[:offset]
        self.offset = offset

    def set_position(self, position):
        position = position - self.position
        self.rotate(position)
        self.position = position

    def rotate(self, places=1):
        self.position += places
        return_val = False
        if self.position == 26:
            self.position = 0
            return_val = 'forward' # Used to indicate if the next rotor should be moved
        elif self.position == -1:
            self.position = 25
            return_val = 'backward'

        self.front_board = self.front_board[places:] + self.front_board[:places]
        self.back_board = self.back_board[places:] + self.back_board[:places]
        return return_val
