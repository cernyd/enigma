from cfg_handler import Config
from enigma.components import EnigmaFactory
from glob import glob
from winsound import PlaySound, SND_ASYNC
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


class DataHandler:
    def __init__(self, master):
        self.global_cfg = Config('config.xml')
        self.global_cfg.focus_buffer('globals')
        self.master = master
        self.enigma_factory = EnigmaFactory(['enigma', 'historical_data.xml'])
        self.enigma = self.enigma_factory.produce_enigma(**self.enigma_cfg, master=master)
        self.playback = Playback(master)

    def switch_enigma(self, model):
        self.enigma = self.enigma_factory.produce_enigma(model, master=self)

    @property
    def font(self):
        return list(self.global_cfg.find('font').values())

    @property
    def bg(self):
        return self.global_cfg.find('bg')['color']

    @property
    def enigma_cfg(self):
        return self.global_cfg.find('enigma_defaults')

    @property
    def settings_vars(self):
        return self.global_cfg.find('setting_vars')