from misc import get_label, alphabet

class Rotor:
    """Class simulating (fairly) accurate enigma machine rotor behavior"""
    def __init__(self, wiring: str, turnover: int = 0, position: int = 0, setting: int = 0):
        """
        :param wiring: Defines how letters are wired back and forth
        :param turnover: Sets on which indicator letter the next rotor is turned
        :param position: Rotor position relative to input
        :param setting: Label indicator relative to internal wiring
        """
        assert(len(wiring) == 26 and type(wiring) == str), 'Invalid wiring "%s"' % wiring

        self.__front_board = alphabet
        self.__back_board = wiring

        self.__position = position
        self.position = position

        self.__ring_setting = setting
        self.ring_setting = setting

        self.__turnover = turnover

    # Label for the rotor menu

    def label(self) -> str:
        return get_label(self.__back_board)

    # Routing functions

    def forward(self, letter: str) -> str:
        """
        Routes a letter from front side to the back side
        :param letter: Input letter
        :return: Letter routed to the front
        """
        return self.__back_board[alphabet.index(letter)]

    def backward(self, letter: str) -> str:
        """
        Routes a letter from the back side to the front side
        :param letter: Input letter
        :return:  Letter routed to the front
        """
        return alphabet[self.__back_board.index(letter)]

    def rotate(self, places: int = 1) -> bool:
        """
        Rotates rotor by n places ( in any direction )
        :param places: By how many places to rotate ( negative rotates back )
        :return: Info if the next position should be turned over
        """
        assert (places in range(-25, 26)), 'Can\'t rotate by "%d" places...' % places

        self.__position += places

        return_val = False
        if self.__position == 26:
            self.__position = 0
            return_val = True # Used to indicate if the next rotor should be moved
        elif self.__position == -1:
            self.__position = 25
            return_val = True

        self.__front_board = self.__front_board[places:] + self.__front_board[:places]
        self.__back_board = self.__back_board[places:] + self.__back_board[:places]

        return return_val

    # Ring setting property

    @property
    def ring_setting(self) -> int:
        """
        Property returning the private ring setting
        :return: Ring offset setting
        """
        return self.__ring_setting

    @ring_setting.setter
    def ring_setting(self, setting: int):
        """
        Sets ring setting ( wiring offset relative to the position indicator numbers )
        :param setting: Wiring offset relative to the indicator letters
        """
        assert (setting in range(0, 25)), 'Invalid ring setting "%d"...' % setting

        setting -= self.__ring_setting
        self.__back_board = self.__back_board = self.__back_board[setting:] + self.__back_board[:setting]
        self.__ring_setting = setting

    # Position property

    @property
    def position(self) -> int:
        """
        Property returning the private rotor position
        :return: Current position
        """
        return self.__position

    @position.setter
    def position(self, position: int):
        """
        Sets rotor to the selected position instantly
        :param position: Target position
        """
        assert(position in range(0, 26)), 'Invalid position "%d"...' % position

        position -= self.__position
        self.rotate(position)
        self.__position = position
