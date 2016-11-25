from misc import get_label, alphabet


class Rotor:
    """Class simulating (fairly) accurate enigma rotor behavior"""
    def __init__(self, wiring, turnover=0, position=0, setting=0):
        """
        wiring - determines how front side is wired to the back side
        turnover - number that will be shown on the indicator on next rotor advance
        position - position offset ( changes after each rotation )
        setting - ring setting ( wiring offset relative to the position indicator numbers )
        """
        self.label = get_label(wiring)
        self.front_board = alphabet
        self.back_board = wiring
        self.position = position
        self.ring_setting = setting
        self.turnover=turnover

    def forward(self, letter):
        """Routes a letter from front side to the back side"""
        return self.back_board[alphabet.index(letter)]

    def backward(self, letter):
        """Routes a letter from the back side to the front side"""
        return alphabet[self.back_board.index(letter)]

    def set_ring_setting(self, setting):
        """Sets ring setting ( wiring offset relative to the position indicator numbers )"""
        setting = setting - self.ring_setting
        self.back_board = self.back_board = self.back_board[
                                            setting:] + self.back_board[:setting]
        self.ring_setting = setting

    def set_position(self, position):
        """Way of instantly setting the rotor to any position"""
        position = position - self.position
        self.rotate(position)
        self.position = position

    def rotate(self, places=1):  # Adjust for notch/turnover positions!
        """Rotates rotor by n places ( in any direction )"""
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
