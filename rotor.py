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
        self._position = position
        self._ring_setting = setting
        self.turnover=turnover

    def forward(self, letter):
        """Routes a letter from front side to the back side"""
        return self.back_board[alphabet.index(letter)]

    def backward(self, letter):
        """Routes a letter from the back side to the front side"""
        return alphabet[self.back_board.index(letter)]

    @property
    def ring_setting(self):
        return self._ring_setting

    @ring_setting.setter
    def ring_setting(self, setting):
        """Sets ring setting ( wiring offset relative to the position indicator numbers )"""
        setting = setting - self._ring_setting
        self.back_board = self.back_board = self.back_board[
                                            setting:] + self.back_board[:setting]
        self._ring_setting = setting

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        """Way of instantly setting the rotor to any position"""
        position = position - self._position
        self.rotate(position)
        self._position = position

    def rotate(self, places=1):  # Adjust for notch/turnover positions!
        """Rotates rotor by n places ( in any direction )"""
        self._position += places

        return_val = False
        if self._position == 26:
            self._position = 0
            return_val = True # Used to indicate if the next rotor should be moved
        elif self._position == -1:
            self._position = 25
            return_val = True

        self.front_board = self.front_board[places:] + self.front_board[:places]
        self.back_board = self.back_board[places:] + self.back_board[:places]
        return return_val
