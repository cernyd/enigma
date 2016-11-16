from winsound import PlaySound, SND_ASYNC
from glob import glob
from os import path


class Playback:
    sound_enabled = True
    sounds = list(map(lambda snd: snd[7:], glob(path.join('sounds', '*.wav'))))

    @classmethod
    def play(cls, sound_name):
        sound_name += '.wav'

        if sound_name in cls.sounds and cls.sound_enabled:
            PlaySound(path.join('sounds', sound_name), SND_ASYNC)
