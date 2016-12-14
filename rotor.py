from misc import get_label, alphabet


class RotorBase:
    def __init__(self, wiring=''):
        self.front_board = alphabet
        self.back_board = wiring
        self.label = get_label(wiring)

    def forward(self, letter: str) -> str:
        """
        Routes a letter from front side to the back side
        :param letter: Input letter
        :return: Letter routed to the front
        """
        return self.back_board[alphabet.index(letter)]

    def backward(self, letter: str) -> str:
        """
        Routes a letter from the back side to the front side
        :param letter: Input letter
        :return:  Letter routed to the front
        """
        return alphabet[self.back_board.index(letter)]

    def dump_config(self):
        """Dumps rotor configuration data"""
        return dict(wiring=self.back_board)
        # return dict(wiring=self.__back_board,
        #             ring_setting=self.__ring_setting,
        #             position=self.__position,
        #             turnover=self.turnover)

    def load_config(self, data):
        """Loads rotor configuration data"""
        self.back_board = data['wiring']
        # self.__back_board = data['wiring']
        # self.turnover = data['turnover']
        # self.ring_setting = data['ring_setting']
        # self.position = data['position']


class Reflector(RotorBase):
    pass


class Rotor(RotorBase):
    def __init__(self, wiring='', turnover=0, position=0, setting=0, config_data=None):
        """
        :param wiring: Defines how letters are wired back and forth
        :param turnover: Sets on which indicator letter the next rotor is turned
        :param position: Rotor position relative to input
        :param setting: Label indicator relative to internal wiring
        """
        RotorBase.__init__(self, wiring)

        self.turnover = turnover
        self.position = position
        self.setting = setting
        self.last_position = 0

        if config_data:
            pass

    def rotate(self, places: int = 1) -> bool:
        """
        Rotates rotor by n places ( in any direction )
        :param places: By how many places to rotate ( negative rotates back )
        :return: Info if the next position should be turned over
        """
        assert (places in range(-25, 26)), 'Can\'t rotate by "%d" places...' % places
        self.last_position = self.position
        self.position += places

        return_val = False
        if self.position == 26:
            self.position = 0

        elif self.position == -1:
            self.position = 25

        if self.position == self.turnover:
            return_val = True  # Used to indicate if the next rotor should be moved

        self.front_board = self.front_board[places:] + self.front_board[:places]
        self.back_board = self.back_board[places:] + self.back_board[:places]

        return return_val

    # Ring setting property

    @property
    def ring_setting(self) -> int:
        """
        Property returning the private ring setting
        :return: Ring offset setting
        """
        return self.ring_setting

    @ring_setting.setter
    def ring_setting(self, setting: int):
        """
        Sets ring setting ( wiring offset relative to the position indicator numbers )
        :param setting: Wiring offset relative to the indicator letters
        """
        assert (setting in range(0, 25)), 'Invalid ring setting "%s"...' % str(setting)
        setting -= self.ring_setting
        self.back_board = self.back_board = self.back_board[setting:] + self.back_board[:setting]
        self.ring_setting = setting

    # Position property

    @property
    def position(self) -> int:
        """
        Property returning the private rotor position
        :return: Current position
        """
        return self.position

    @position.setter
    def position(self, position: int):
        """
        Sets rotor to the selected position instantly
        :param position: Target position
        """
        assert(position in range(0, 26)), 'Invalid position "%d"...' % position

        position -= self.position
        self.rotate(position)
        self.position = position
