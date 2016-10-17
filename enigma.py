class Rotor:
    def __init__(self, back_alphabet, position=0, ring_offset=0):
        self.back_alphabet = back_alphabet
        self.front_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.position = position
        self.rotate(self.position)
        self.initial_pos = [self.back_alphabet, self.front_alphabet]

    def reset_rotor(self):
        self.back_alphabet, self.front_alphabet = self.initial_pos

    def route_forward(self, letter):
        return self.back_alphabet[self.front_alphabet.index(letter)]

    def route_backward(self, letter):
        return self.front_alphabet[self.back_alphabet.index(letter)]

    def rotate(self, places=1):
        if places:
            print(self.back_alphabet)
            self.back_alphabet = self.back_alphabet[places:] + \
                                 self.back_alphabet[:places]
            print(self.back_alphabet)

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

        self.rotor_positions = []
        for rotor in self.rotors:
            self.rotor_positions.append(rotor.position)

        self.initial_rotor_pos = self.rotor_positions

    def rotate_first(self):

        rot_next = False

        index = 0
        for _ in self.rotors:
            if index == 0 or rot_next:
                self.rotors[index].rotate()

            if self.rotor_positions[index] == 26:
                self.rotor_positions[index] = 0
                rot_next = True
            else:
                self.rotor_positions[index] += 1
                rot_next = False
            index += 1

    def reset_positions(self):
        self.rotor_positions = self.initial_rotor_pos
        for rotor in self.rotors:
            rotor.reset_rotor()

    def button_press(self, letter):
        self.rotate_first()
        print(self.rotor_positions)
        print('Before etw > ', letter)
        output = self.etw.route_forward(letter)
        print('After etw > ', output)

        for rotor in self.rotors:
            output = rotor.route_forward(output)
            print('Rotor > ', output)

        print('Before reflection > ', output)
        output = self.ukw.reflect(output)
        print('After reflection > ', output)

        for rotor in reversed(self.rotors):
            output = rotor.route_backward(output)
            print('Rotor > ', output)

        print('Before etw > ', output)
        output = self.etw.route_backward(output)
        print('After etw > ', output)

        return output


rotors = Enigma1.rotors


#"""
enigma = Enigma(rotors['ETW'], [rotors['I'], rotors['II'], rotors['III']], rotors['UKW-A'])


output = ''
for letter in 'HELLO':
    output += enigma.button_press(letter)

print('\nOutput: ', output, '\n')
enigma.reset_positions()

output2 = ''
for letter in output:
    output2 += enigma.button_press(letter)

print('\nOutput: ', output2)

