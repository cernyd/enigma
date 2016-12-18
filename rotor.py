from string import ascii_uppercase as alphabet


class RotorBase:
    """Base class for Rotors and Reflectors"""
    def __init__(self, label='', back_board='', turnover='', valid_cfg=tuple()):
        """All parameters except should be passed in **config, valid_cfg is a
        tuple of additional configuration data for config loading and dumping"""
        self.valid_cfg = ['back_board', 'label', 'turnover']
        self.valid_cfg.extend(valid_cfg)
        self.back_board = back_board
        self.turnover = turnover
        self.label = label

    def forward(self, letter):
        """Routes letter from front to back"""
        return self.back_board[alphabet.index(letter)]

    def backward(self, letter):
        """Routes letter from back to front"""
        return alphabet[self.back_board.index(letter)]

    def config(self, **attrs):
        """Loads rotor configuration data"""
        for attr in attrs.keys():
            if attr not in self.valid_cfg:
                raise AttributeError('Invalid attribute "%s"!' % (attr))
            value = attrs.get(attr)
            if value:
                setattr(self, attr, value)

    def dump_config(self):
        """Dumps rotor configuration data"""
        cfg = {}
        for attr in self.valid_cfg:
            cfg[attr] = self.__dict__[attr]
        return cfg

    def __repr__(self):
        """Visualising wiring made easier"""
        return self.back_board


class Reflector(RotorBase):
    """Reflector class, does not overload anything from the RotorBase"""


class Rotor(RotorBase):
    """Inherited from RotorBase, adds rotation and ring setting functionality"""
    def __init__(self, **cfg):
        RotorBase.__init__(self, **cfg, valid_cfg=('position', 'ring_setting'))
        self.ring_setting = 0
        self.position = 0
        self.last_position = 0

    def rotate(self, places=1):
        """Rotates rotor by one x places, returns True if the next rotor should
        be turned over"""
        self.last_position = self.position
        self.position += places

        if self.position == 26:
            self.position = 0
        elif self.position == -1:
            self.position = 25

        self.set_offset(places)
        return self.did_turnover()

    def did_turnover(self):
        """Checks if the next position should turn by one place."""
        if (self.last_position, self.position) == self.turnover:
            return True
        elif (self.position, self.last_position) == self.turnover:
            return True
        return False

    def set_offset(self, places=1):
        """Sets rotor offset relative to the enigma"""
        # self.front_board = self.front_board[places:] + self.front_board[:places]
        self.back_board = self.back_board[places:] + self.back_board[:places]

    def set_ring_setting(self, setting):
        """Sets rotor indicator offset relative to the internal wiring"""
        assert (setting in range(0, 25)), 'Invalid ring setting "%s"...' % str(setting)
        setting -= self.ring_setting
        self.back_board = self.back_board = self.back_board[setting:] + self.back_board[:setting]
        self.ring_setting = setting

    def set_position(self, position):
        """Sets rotor offset position"""
        assert(position in range(0, 26)), 'Invalid position "%d"...' % position

        position -= self.position
        self.rotate(position)
        self.position = position
