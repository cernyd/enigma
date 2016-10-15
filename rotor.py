class Rotor:
    def __init__(self, rotor_label, back_alphabet, rotor_offset=0):
        self.__front_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.__back_alphabet = back_alphabet
        self.rotor_label = rotor_label
        self.rotor_offset = rotor_offset

        self.set_offset(rotor_offset)

    def set_offset(self, rotor_offset):
        temp_routing = []
        back_alph_with_offset = self.__back_alphabet[rotor_offset:] + \
                                self.__back_alphabet[:rotor_offset]
        for input_letter, output_letter in zip(self.__front_alphabet,
                                               back_alph_with_offset):
            temp_routing.append((input_letter, output_letter))

        self.rotor_routing = tuple(temp_routing)

    def route_signal(self, input_letter, side='front'):
        if side == 'front':
            route_idx = self.__front_alphabet.index(input_letter)
            return self.rotor_routing[route_idx][1]
        elif side == 'back':  # Can be used as a reflector too
            route_idx = self.__back_alphabet.index(input_letter)
            return self.rotor_routing[route_idx][0]

    def __str__(self):
        routing = []
        for rotor_route in self.rotor_routing:
            routing.append('{} > {}'.format(*rotor_route))

        return "Rotor label: {}\noffset: {}\nrouting:\n{}".format(self.rotor_label,
                                                                  self.rotor_offset,
                                                          '\n'.join(routing))


class HistoricalRotors:
    """Historically accurate rotors, UKW - Reflector, ETW - Stationary rotor"""

    rotors = {'Commercial Enigma A,B': {
                  'IC': Rotor('IC', 'DMTWSILRUYQNKFEJCAZBPGXOHV'),
                  'IIC': Rotor('IIC', 'HQZGPJTMOBLNCIFDYAWVEUSRKX'),
                  'IIIC': Rotor('IIIC', 'UQNTLSZFMREHDPXKIBVYGJCWOA')},
              'German Railway (Rocket)': {
                  'I': Rotor('IC', 'JGDQOXUSCAMIFRVTPNEWKBLZYH'),
                  'II': Rotor('IIC', 'NTZPSFBOKMWRCJDIVLAEYUXHGQ'),
                  'III': Rotor('IIIC', 'JVIUBHTCDYAKEQZPOSGXNRMWFL'),
                  'UKW': Rotor('UKW', 'QYHOGNECVPUZTFDJAXWMKISRBL'),
                  'ETW': Rotor('ETW', 'QWERTZUIOASDFGHJKPYXCVBNML')},
              'Swiss K': {
                  'I-K': Rotor('I-K', 'PEZUOHXSCVFMTBGLRINQJWAYDK'),
                  'II-K': Rotor('II-K', 'ZOUESYDKFWPCIQXHMVBLGNJRAT'),
                  'III-K': Rotor('III-K', 'EHRVXGAOBQUSIMZFLYNWKTPDJC'),
                  'UKW-K': Rotor('UKW-K', 'IMETCGFRAYSQBZXWLHKDVUPOJN'),
                  'ETW-K': Rotor('ETW-K', 'QWERTZUIOASDFGHJKPYXCVBNML')},
              'Enigma I': {
                  'I': Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'),
                  'II': Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE'),
                  'III': Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO')},
              'M3 Army': {
                  'IV': Rotor('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB'),
                  'V': Rotor('V', 'VZBRGITYUPSDNHLXAWMJQOFECK')},
              'M3 & M4 Naval': {
                  'VI': Rotor('VI', 'JPGVOUMFYQBENHZRDKASXLICTW'),
                  'VII': Rotor('VII', 'NZJHGRCXMYSWBOUFAIVLPEKQDT'),
                  'VIII': Rotor('VIII', 'FKQHTLXOCBJSPDZRAMEWNIUYGV')},
              }


class Enigma1:
    """
    Historically accurate Enigma 1 rotor wiring
    UKW - Reflector
    ETW - Stationary router
    """

    rotors = {
              'ETW': Rotor('ETW', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
              'I': Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'),
              'II': Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE'),
              'III': Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO'),
              'IV': Rotor('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB'),
              'V': Rotor('V', 'VZBRGITYUPSDNHLXAWMJQOFECK'),
              'UKW-A': Rotor('UKW-A', 'EJMZALYXVBWFCRQUONTSPIKHGD'),
              'UKW-B': Rotor('UKW-B', 'YRUHQSLDPXNGOKMIEBFZCWVJAT'),
              'UKW-C': Rotor('UKW-C', 'FVPJIAOYEDRZXWGCTKUQSBNMHL')
              }
