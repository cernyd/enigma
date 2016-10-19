alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Rotor:  # 26 letters in alphabet!
    def __init__(self, wiring, position=0, offset=0):
        self.front_board = alphabet
        self.back_board = wiring
        self.position = position
        self.offset = offset

    def forward(self, letter):
        return self.back_board[alphabet.index(letter)]

    def backward(self, letter):
        return alphabet[self.back_board.index(letter)]

    def reset(self):
        self.rotate(26 - self.position)
        self.set_offset(26 - self.offset)
        self.position = 0
        self.offset = 0

    def set_offset(self, offset):
        offset = offset - self.offset
        self.back_board = self.back_board = self.back_board[offset:] + self.back_board[:offset]
        self.offset = offset

    def set_position(self, position):
        position = position - self.position
        self.rotate(position)
        self.position = position

    def rotate(self, places=1):
        if self.position == 26:
            self.position = 0
            return True
        else:
            self.position += 1

        self.front_board = self.front_board[places:] + self.front_board[:places]
        self.back_board = self.back_board[places:] + self.back_board[:places]
