from base64 import b85encode, b85decode
from pickle import dumps, loads


def load_config():
    with open('settings.txt', 'rb') as data:
        data = data.read()
        decoded = b85decode(data)
        return loads(decoded)

def save_config(config_data):
    with open('settings.txt', 'wb') as file:
        pickled = dumps(config_data)
        encoded = b85encode(pickled)
        file.write(encoded)
