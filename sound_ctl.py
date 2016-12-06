from winsound import PlaySound, SND_ASYNC
from glob import glob
from os import path


class Playback:
    """Module for playing sounds from the sounds folder"""

    def __init__(self, master_instance):
        self.sounds = list(
            map(lambda snd: snd[7:], glob(path.join('sounds', '*.wav'))))
        self.master_instance = master_instance

    def play(self, sound_name):
        """Plays a sound based on the entered sound name"""
        sound_name += '.wav'

        if sound_name in self.sounds and self.master_instance.sound_enabled:
            PlaySound(path.join('sounds', sound_name), SND_ASYNC)
