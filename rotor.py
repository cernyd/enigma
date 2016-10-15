class HistoricalRotors:
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


class Rotor:
    def __init__(self, rotor_label, back_alphabet, rotor_position=1):
        self.__front_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.__back_alphabet = back_alphabet

        self.rotor_label = rotor_label
        self.__rotor_position = rotor_position  # Default position

        temp_routing = []
        for input_letter, output_letter in zip(self.__front_alphabet,
                                               self.__back_alphabet):
            temp_routing.append((input_letter, output_letter))

        self.rotor_routing = tuple(temp_routing)

    def set_rotor_position(self, rotor_position):
        self.__rotor_position = rotor_position

    def rotate(self):
        if self.__rotor_position == 26:
            self.__rotor_position = 1
            return True  # Rotate next rotor
        else:
            self.__rotor_position += 1
            return False  # Do not rotate next rotor

    def route_signal(self, input_letter, side='front'):
        if side == 'front':
            route_idx = self.__front_alphabet.index(input_letter)
            return self.rotor_routing[route_idx][1]
        elif side == 'back':
            route_idx = self.__back_alphabet.index(input_letter)
            return self.rotor_routing[route_idx][0]
