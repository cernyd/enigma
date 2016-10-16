class Rotor:
    def __init__(self, back_alphabet, position=0, ring_offset=0):
        self.back_alphabet = back_alphabet
        self.front_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.position = position

    def route_forward(self, letter):
        return self.back_alphabet[self.front_alphabet.index(letter)]

    def route_backward(self, letter):
        return self.front_alphabet[self.back_alphabet.index(letter)]

    def rotate(self):
        self.back_alphabet = self.back_alphabet[:1] + self.back_alphabet[1:]

    def set_ring_offset(self, offset):
        self.front_alphabet = self.front_alphabet[:offset] + self.front_alphabet[offset:]


class Reflector:
    def __init__(self, back_alphabet, position=0, ring_offset=0):
        self.back_alphabet = back_alphabet
        self.front_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.position = position

    def reflect(self, letter):
        return self.front_alphabet[self.back_alphabet.index(letter)]


class Enigma1:
    """
    Historically accurate Enigma 1 rotor wiring
    UKW - Reflector
    ETW - Stationary router
    """
    rotors = {
              'ETW': Rotor('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
              'I': Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ'),
              'II': Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE'),
              'III': Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO'),
              'IV': Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB'),
              'V': Rotor('VZBRGITYUPSDNHLXAWMJQOFECK'),
              'UKW-A': Reflector('EJMZALYXVBWFCRQUONTSPIKHGD'),
              'UKW-B': Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT'),
              'UKW-C': Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
              }


class Enigma:
    def __init__(self, etw, rotors, ukw, plugboard=None):
        self.etw = etw
        self.rotors = rotors
        self.ukw = ukw

    def button_press(self, letter):
        output = self.etw.route_forward(letter)

        for rotor in self.rotors:
            output = rotor.route_forward(output)
        print('Before reflection > ', output)

        output = self.ukw.reflect(output)

        print('After reflection > ', output)
        for rotor in reversed(self.rotors):
            output = rotor.route_backward(output)

        output = self.etw.route_backward(letter)

        return output



rotors = Enigma1.rotors

"""
enigma = Enigma(rotors['ETW'], [rotors['III'], rotors['II'], rotors['I']], rotors['UKW-A'])


output = ''
for letter in 'HELLO':
    output += enigma.button_press(letter)

print('\nOutput: ', output, '\n')

output2 = ''
for letter in output:
    output2 += enigma.button_press(letter)

print('\nOutput: ', output2)
"""
