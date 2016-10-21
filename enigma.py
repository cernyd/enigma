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
                if rotate_next:
                    rotate_next = rotor.rotate()
                else:
                    break
            index += 1

    def prt_positions(self):
        print(self.rotors[0].position, self.rotors[1].position, self.rotors[2].position)

    def reset(self):
        for rotor in self.rotors:
            rotor.reset()

    def button_press(self, letter):
        self.rotate_primary()
        self.prt_positions()
        output = letter;print('Input > ', output)

        for rotor in self.rotors:
            output = rotor.forward(output);print('Forward > ', output)

        output = self.reflector.forward(output);print('Reflection > ', output)

        for rotor in reversed(self.rotors):
            output = rotor.backward(output);print('Backward > ', output)
        print('Output > ', output)
        return output
