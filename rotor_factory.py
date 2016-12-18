from rotor import Rotor, Reflector


class DataStorage:
    _labels = ('A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06',
                'G-07', 'H-08', 'I-09', 'J-10', 'K-11', 'L-12',
                'M-13', 'N-14', 'O-15', 'P-16', 'Q-17', 'R-18',
                'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24',
                'Y-25', 'Z-26')

    _layout = ((16, 22, 4, 17, 19, 25, 20, 8, 14),
               (0, 18, 3, 5, 6, 7, 9, 10),
               (15, 24, 23, 2, 21, 1, 13, 12, 11))

    _factory_data = {'Enigma1':
                          {'rotor': [
                              ('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', (16, 17)),
                              ('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', (12, 13)),
                              ('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', (3, 4)),
                              ('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', (17, 18)),
                              ('V', 'VZBRGITYUPSDNHLXAWMJQOFECK', (7, 8))],
                           'reflector': [
                               ('UKW-A', 'EJMZALYXVBWFCRQUONTSPIKHGD'),
                               ('UKW-B', 'YRUHQSLDPXNGOKMIEBFZCWVJAT'),
                               ('UKW-C', 'FVPJIAOYEDRZXWGCTKUQSBNMHL')]}}

    _factory_data.update(labels=_labels)
    _factory_data.update(layout=_layout)

    def __new__(cls):
        raise NotImplementedError('This class was not intended for instantiation!')

    @classmethod
    def get_info(cls, data_type, rotor_type=None):
        if rotor_type:
            return [config[0] for config in
                    cls._factory_data[data_type][rotor_type]]
        else:
            return cls._factory_data[data_type]

    @classmethod
    def _create_cfg(cls, label, back_board, turnover=None):
        """Creates a configuration dictionary"""
        cfg = dict(label=label, back_board=back_board)
        if turnover:
            cfg.update(turnover=turnover)
        return cfg


class RotorFactory(DataStorage):
    """Factory for creating various enigma Rotor/Reflector objects"""
    def __new__(cls):
        raise NotImplementedError('This class was not intended for instantiation!')

    @classmethod
    def produce(cls, model, rotor_type, label):
        """Creates and returns new object based on input"""
        cfg = None

        for item in cls._factory_data[model][rotor_type]:
            if item[0] == label:
                cfg = cls._create_cfg(*item)
                break

        if cfg:
            if rotor_type == 'rotor':
                return  Rotor(**cfg)
            elif rotor_type == 'reflector':
                return  Reflector(**cfg)
        else:
            raise AttributeError('No configuration found for "%s" > "%s" > "%s"!'
                                 % (model, rotor_type, label))
