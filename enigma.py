from rotor import Rotor
from historical import Enigma1


class Enigma:
    def __init__(self, reflector, rotors):
        self.reflector = reflector
        self.rotors = rotors

    def rotate_primary(self):
        rotate_next = False
        index = 0
        for rotor in self.rotors:
            if rotate_next or index == 0:
                rotate_next = rotor.rotate()
            index += 1

    def prt_positions(self):
        print(self.rotors[0].position, self.rotors[1].position, self.rotors[2].position)

    def reset(self):
        for rotor in self.rotors:
            rotor.reset()

    def button_press(self, letter):
        self.rotate_primary()
        self.prt_positions()
        output = letter

        for rotor in self.rotors:
            output = rotor.forward(output)

        output = self.reflector.forward(output)

        for rotor in reversed(self.rotors):
            output = rotor.backward(output)

        return output


rotors = Enigma1.rotors
enigma = Enigma(Rotor(rotors['UKW-B']),[Rotor(rotors['III']),Rotor(rotors['II']),Rotor(rotors['I'])])

output = ''
for letter in 'A':
    output += enigma.button_press(letter)

print(output)

enigma.reset()

output2 = ''
for letter in output:
    output2 += enigma.button_press(letter)

print(output2)
