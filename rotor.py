from misc import get_label, alphabet

"""Rotorbase class really confusing as to how does it initiate everything."""



class RotorBase:
    def __init__(self, wiring=''):
        self.front_board = alphabet
        self.back_board = wiring
        self.label = get_label(wiring)

    def forward(self, letter: str) -> str:
        return self.back_board[alphabet.index(letter)]

    def backward(self, letter: str) -> str:
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
        RotorBase.__init__(self, wiring)

        self.turnover = turnover
        self.position = position
        self.ring_setting = setting
        self.last_position = 0

        if config_data:
            pass

    def rotate(self, places: int = 1) -> bool:
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

    def set_ring_setting(self, setting: int):
        assert (setting in range(0, 25)), 'Invalid ring setting "%s"...' % str(setting)
        setting -= self.ring_setting
        self.back_board = self.back_board = self.back_board[setting:] + self.back_board[:setting]
        self.ring_setting = setting

    def set_position(self, position: int):
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
