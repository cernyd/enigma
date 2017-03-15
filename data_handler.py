from cfg_handler import Config


class DataHandler:
    def __init__(self):
        self.enigma = None
        config = Config('config.xml')
        config.focus_buffer('globals')
        config.find('font')
        font = list(config.find('font').values())
        bg = config.find('bg')['color']
        enigma_cfg = config.find('enigma_defaults')