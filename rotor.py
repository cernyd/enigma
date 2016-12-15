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

    def load_config(self, data):
        """Loads rotor configuration data"""
        self.__init__(data['wiring'])

    def __repr__(self):
        return self.back_board


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
        self.ring_setting = setting
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

    def set_ring_setting(self, setting: int):
        """
        Sets ring setting ( wiring offset relative to the position indicator numbers )
        :param setting: Wiring offset relative to the indicator letters
        """
        assert (setting in range(0, 25)), 'Invalid ring setting "%s"...' % str(setting)
        setting -= self.ring_setting
        self.back_board = self.back_board = self.back_board[setting:] + self.back_board[:setting]
        self.ring_setting = setting

    # Position property

    def set_position(self, position: int):
        """
        Sets rotor to the selected position instantly
        :param position: Target position
        """
        assert(position in range(0, 26)), 'Invalid position "%d"...' % position

        position -= self.position
        self.rotate(position)
        self.position = position

    def dump_config(self):
        config = RotorBase.dump_config(self)
        config.update(dict(wiring=self.back_board,
                           ring_setting=self.ring_setting,
                           position=self.position,
                           turnover=self.turnover))
        return config

    def load_config(self, config):
        RotorBase.load_config(self, config)
        for key, value in config.items():
            setattr(self, key, value)
