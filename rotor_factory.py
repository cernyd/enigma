from rotor import Rotor, Reflector


class RotorFactory:
    """Factory for creating various enigma Rotor/Reflector objects"""
    __factory_data = {'Enigma1':
                          {'rotor': [('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', (16, 17)),
                                     ('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', (12, 13)),
                                     ('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', (3, 4)),
                                     ('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', (17, 18)),
                                     ('V', 'VZBRGITYUPSDNHLXAWMJQOFECK', (7, 8))],
                           'reflector': [('UKW-A', 'EJMZALYXVBWFCRQUONTSPIKHGD'),
                                         ('UKW-B', 'YRUHQSLDPXNGOKMIEBFZCWVJAT'),
                                         ('UKW-C', 'FVPJIAOYEDRZXWGCTKUQSBNMHL')]}}

    def __new__(cls):
        raise NotImplementedError('This class was not intended for instantiation!')

    @classmethod
    def produce(cls, model, rotor_type, label):
        """Creates and returns new object based on input"""
        cfg = None

        for item in cls.__factory_data[model][rotor_type]:
            if item[0] == label:
                cfg = cls.__create_cfg(*item)
                break

        if cfg:
            if rotor_type == 'rotor':
                return  Rotor(**cfg)
            elif rotor_type == 'reflector':
                return  Reflector(**cfg)
        else:
            raise AttributeError('No configuration found for "%s" > "%s" > "%s"!'
                                 % (model, rotor_type, label))

    @classmethod
    def __create_cfg(cls, label, back_board, turnover=None):
        """Creates a configuration dictionary"""
        cfg = dict(label=label, back_board=back_board)
        if turnover:
            cfg.update(turnover=turnover)
        return cfg
