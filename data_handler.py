from cfg_handler import Config


class DataHandler:
    def __init__(self):
        self.enigma = None
        self.global_cfg = Config('config.xml')
        self.global_cfg.focus_buffer('globals')

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