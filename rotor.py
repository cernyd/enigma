from string import ascii_uppercase as alphabet


class RotorBase:
    """Base class for Rotors and Reflectors"""
    def __init__(self, label='', back_board='', turnover='', valid_cfg=tuple()):
        """All parameters except should be passed in **config, valid_cfg is a
        tuple of additional configuration data for config loading and dumping"""
        self.valid_cfg = ['back_board', 'label', 'turnover', 'relative_board',
                          'position_ring']
        self.valid_cfg.extend(valid_cfg)

        # Necessary config data
        self.position_ring = alphabet # list(range(1,27))
        self.back_board = back_board
        self.relative_board = alphabet
        self.turnover = turnover
        self.label = label

    def relative_input(self, letter):
        """Convert absolute input to relative input"""
        return self.relative_board[alphabet.index(letter)]

    def absolute_output(self, routed_output):
        """Relative output to absolute output"""
        return alphabet[self.relative_board.index(routed_output)]

    def visualise(self, info, mode='forward'):
        """Visualises how the rotor works"""
        info = info[::-1]
        boards = [alphabet, self.relative_board, self.relative_board, alphabet]
        index = 0
        for _ in alphabet:
            curr_line = []
            for symb, board in zip(info, boards):
                if symb == board[index]:
                    curr_line.append('<- ' + board[index])
                else:
                    curr_line.append('   ' + board[index])
            letter = self.position_ring[index]
            indicator = ' %s ' % letter if index != 0 else '[%s]' % letter
            curr_line.insert(1, indicator)
            print("{} ||{}||{} {} | {}".format(*curr_line))
            index += 1

    def forward(self, letter):
        """Routes letter from front to back"""
        info = []
        info.append(letter)
        relative_input = self.relative_input(letter)
        info.append(relative_input)
        routed_output = self.back_board[alphabet.index(relative_input)]
        info.append(routed_output)
        info.append(self.absolute_output(routed_output))
        self.visualise(info)
        return self.absolute_output(routed_output)

    def backward(self, letter):
        """Routes letter from back to front"""
        relative_entry = self.relative_input(letter)
        routed_output = alphabet[self.back_board.index(relative_entry)]
        return self.absolute_output(routed_output)

    def config(self, **attrs):
        """Loads rotor configuration data"""
        for attr in attrs.keys():
            if attr not in self.valid_cfg:
                raise AttributeError('Invalid attribute "%s"!' % attr)
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


# here: http://users.telenet.be/d.rijmenants/en/enigmatech.htm


class Rotor(RotorBase):
    """Inherited from RotorBase, adds rotation and ring setting functionality"""
    def __init__(self, **cfg):
        RotorBase.__init__(self, **cfg, valid_cfg=('position', ))
        self.last_position = None
        self.position = self.position_ring[0]

    def rotate(self, places=1):
        """Rotates rotor by one x places, returns True if the next rotor should
        be turned over"""
        self.change_offset(places)
        return self.did_turnover()

    def did_turnover(self):
        """Checks if the next position should turn by one place."""
        if (self.last_position, self.position) == self.turnover:
            return True
        elif (self.position, self.last_position) == self.turnover:
            return True
        return False

    def change_offset(self, places=1):
        """Sets rotor offset relative to the enigma"""
        self.last_position = self.relative_board[0]
        self.relative_board = self.relative_board[places:] + \
                              self.relative_board[:places]
        self.position_ring = self.position_ring[places:] + \
                              self.position_ring[:places]
        self.position = self.relative_board[0]

    def set_position(self, position):
        while self.position_ring[0] != position:
            self.change_offset()

    def get_ring_setting(self):
        return self.position_ring[self.relative_board.index('A')]

    def set_ring_setting(self, setting):
        """Sets rotor indicator offset relative to the internal wiring"""
        while self.position_ring.index(setting) != self.relative_board.index('A'):
            self.relative_board = self.relative_board[1:] + \
                                  self.relative_board[:1]
