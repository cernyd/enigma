from historical import Enigma1

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_label(wiring):
    for key, value in Enigma1.rotors.items():
        if value[0] == wiring:
            return key
        elif value == wiring:
            return key


class Rotor:  # 26 letters in alphabet!
    def __init__(self, wiring, turnover=0, position=0, setting=0):
        self.label = get_label(wiring)
        self.front_board = alphabet
        self.back_board = wiring
        self.position = position
        self.ring_setting = setting
        self.turnover=turnover

    def forward(self, letter):
        return self.back_board[alphabet.index(letter)]

    def backward(self, letter):
        return alphabet[self.back_board.index(letter)]

    def set_ring_setting(self, setting):
        setting = setting - self.ring_setting
        self.back_board = self.back_board = self.back_board[
                                            setting:] + self.back_board[:setting]
        self.ring_setting = setting

    def set_position(self, position):
        position = position - self.position
        self.rotate(position)
        self.position = position

    def rotate(self, places=1):  # Adjust for notch/turnover positions!
        self.position += places

        return_val = False
        if self.position == 26:
            self.position = 0
            return_val = True # Used to indicate if the next rotor should be moved
        elif self.position == -1:
            self.position = 25
            return_val = True

        self.front_board = self.front_board[places:] + self.front_board[:places]
        self.back_board = self.back_board[places:] + self.back_board[:places]
        return return_val
