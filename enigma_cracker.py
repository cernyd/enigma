from itertools import product, permutations
from string import ascii_uppercase as alphabet
from enigma.components import BasicEnigma1, RotorFactory
from time import time

def crack_positions(model, cipher, crib):
    t1 = time()
    factory = RotorFactory(['enigma', 'historical_data.xml'], model)
    all_rotors = [factory.produce('rotors', label) for label in ('I', 'II', 'III', 'IV', 'V')]
    stator = factory.produce('stators', 'ETW')
    enigma = BasicEnigma1('', factory.produce('reflectors', 'UKW-B'), [factory.produce('rotors', label) for label in ['I', 'II', 'III']], stator)
    setting_permutations = list(product(alphabet, repeat=3))
    order_permutations = list(permutations(all_rotors, r=3))

    for reflector in [factory.produce('reflectors', reflector) for reflector in ('UKW-B', 'UKW-A', 'UKW-C')]:
        enigma.reflector = reflector

        for rotor_order in order_permutations:
            enigma.rotors = rotor_order

            for setting in setting_permutations:
                enigma.positions = setting

                for index in range(len(cipher)):
                    if enigma.button_press(cipher[index]) != crib[index]:
                        break
                    if index == len(cipher) - 1:
                        t2 = time()
                        return enigma.reflector.label, enigma.rotor_labels, setting, t2 - t1


def guess_plug_pairs(cipher, crib):
    pairs = []
    for index in range(len(cipher)):
        if cipher[index] != crib[index]:
            pair = cipher[index] + crib[index]
            if pair not in pairs:
                pairs.append(pair)
    return pairs
