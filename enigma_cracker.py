from itertools import product, permutations
from string import ascii_uppercase as alphabet
from enigma.components import Enigma1, RotorFactory
from time import time

def crack_positions(model, cipher, crib):
    rotor_perms = list(product(alphabet, repeat=3))
    factory = RotorFactory(['enigma', 'historical_data.xml'], model)
    reflector = factory.produce('reflectors', 'UKW-B')
    stator = factory.produce('stators', 'ETW')
    enigma = Enigma1('', reflector, [factory.produce('rotors', label) for label in ['I', 'II', 'III']], stator)

    t1 = time()
    for rotor_order in permutations(['I', 'II', 'III', 'IV', 'V'], r=3):
        enigma.rotors = [factory.produce('rotors', label) for label in rotor_order]
        for setting in rotor_perms:
            return_setting = False
            enigma.positions = setting

            for index in range(len(cipher)):
                if enigma.button_press(cipher[index]) != crib[index]:
                    break
                if index == len(cipher) - 1:
                    return_setting = True

            if return_setting:
                t2 = time()
                return rotor_order, setting, t2 - t1


def guess_plug_pairs(cipher, crib):
    pairs = []
    for index in range(len(cipher)):
        if cipher[index] != crib[index]:
            pair = cipher[index] + crib[index]
            if pair not in pairs:
                pairs.append(pair)
    return pairs

