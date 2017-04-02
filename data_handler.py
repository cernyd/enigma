from enigma.components import EnigmaFactory
from winsound import PlaySound, SND_ASYNC
from cfg_handler import Config
from glob import glob
from os import path
from tkinter import messagebox


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
    """Holds all up to date data and distributes it accross the whole program"""
    def __init__(self, master=None):
        self.global_cfg = Config('config.xml')
        self.global_cfg.focus_buffer('globals')
        self.master = master
        self.enigma_factory = EnigmaFactory(['enigma', 'historical_data.xml'])
        self.enigma = None
        self.playback = Playback(master)
        self.switch_enigma()

    def switch_enigma(self, model='Enigma1', **config):
        """Switches current enigma model"""
        if self.master:
            self.enigma = self.enigma_factory.produce_enigma(model, **config,
                                                             master=self.master)
        else:
            self.enigma = self.enigma_factory.produce_enigma(model, **config)

    def set_master(self, master):
        """Sets datahandler gui tkinter master"""
        self.master = master
        self.playback.master_instance = master
        self.switch_enigma()

    @property
    def font(self):
        """Returns font from config"""
        font = self.global_cfg.find('font')
        return font['style'], font['size']

    @property
    def bg(self):
        """Returns background color from config"""
        return self.global_cfg.find('bg')['color']

    @property
    def enigma_cfg(self):
        """Returns default enigma settings"""
        return self.global_cfg.find('enigma_defaults')

    @property
    def settings_vars(self):
        """Returns setting variables for gui"""
        return self.global_cfg.find('setting_vars')

    def save_config(self):
        """Saves all important configuration to the global_cfg file"""
        data = dict(gui=dict(sound_enabled=str(self.master.sound_enabled),
                    autorotate=str(self.master.autorotate),
                    rotor_lock=str(self.master.rotor_lock),
                    synchronised_scrolling=str(self.master.sync_scroll),
                    show_numbers=str(self.master.show_numbers)),
                    enigma=dict(self.enigma.dump_config()))

        self.global_cfg.clear_children('saved')

        self.global_cfg.new_subelement('saved', 'gui', toint='*', **data['gui'])

        split = 'rotors uhr_pairs normal_pairs ' \
                'rotor_positions ring_settings reflector_pairs'

        self.global_cfg.new_subelement('saved', 'enigma', split=split,
                                       toint='uhr_position', **data['enigma'])

        self.global_cfg.focus_buffer('globals')

        self.global_cfg.write()

    def load_config(self):
        """Returns data for configuration loading"""
        self.global_cfg.clear_focus()
        data = None
        try:
            self.global_cfg.focus_buffer('saved')
            data = dict(enigma=self.global_cfg.find('enigma'),
                        gui=self.global_cfg.find('gui'))
        except AssertionError:
            messagebox.showerror('Configuration loading error',
                                 'No configuration available')
        finally:
            self.global_cfg.focus_buffer('globals')
            return data

    def remove_config(self):
        """Clears configuration data"""
        self.global_cfg.clear_focus()
        self.global_cfg.clear_children('saved')
        self.global_cfg.focus_buffer('globals')
        self.global_cfg.write()
