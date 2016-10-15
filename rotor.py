from string import ascii_uppercase


class Rotor:
    def __init__(self, rotor_label, rotor_routing,rotor_position=1):
        self.rotor_label = rotor_label
        self.rotor_position = rotor_position  # Default position

        temp_routing = []
        for input_letter, output_letter in zip(ascii_uppercase, rotor_routing):
            temp_routing.append((input_letter, output_letter))
        self.rotor_routing = tuple(temp_routing)

    def rotate(self):
        if self.rotor_position == 26:
            self.rotor_position = 1
            return True  # Rotate next rotor
        else:
            self.rotor_position += 1
            return False  # Do not rotate next rotor

    def route_signal(self, input_letter):
        route_idx = ascii_uppercase.index(input_letter)
        return self.rotor_routing[route_idx][1]


IC = Rotor('IC', 'DMTWSILRUYQNKFEJCAZBPGXOHV')
print(IC.rotor_routing)
print(IC.route_signal('X'))