from os import remove
from tkinter import Menu
from webbrowser import open as open_browser


class RootMenu(Menu):
    def __init__(self, master, *args, **kwargs):
        Menu.__init__(self, master, *args, **kwargs)

        settings_menu = Menu(self, tearoff=0)
        self.add_cascade(label='Settings', menu=settings_menu)
        self.add_command(label='About', command=lambda: open_browser(
            'https://github.com/cernyd/enigma'))
        self.add_command(label='Help')
        config_menu = Menu(settings_menu, tearoff=0)

        config_menu.add_command(label='Save Configuration',
                                command=self.master.save_config)
        config_menu.add_command(label='Load Configuration',
                                command=self.master.load_config)
        config_menu.add_command(label='Delete Configuration',
                                command=lambda: remove('settings.txt'))

        settings_menu.add_cascade(label='Saving and Loading', menu=config_menu)

        settings_menu.add_separator()
        settings_menu.add_checkbutton(label='Enable sound', onvalue=1, offvalue=0,
                                      variable=self.master._sound_enabled)
        settings_menu.add_checkbutton(label='Autorotate',
                                      variable=self.master._autorotate)
        settings_menu.add_checkbutton(label='Rotor lock',
                                      variable=self.master._rotor_lock)
        settings_menu.add_checkbutton(label='Synchronised scrolling',
                                      variable=self.master._sync_scroll)
        settings_menu.add_separator()
        settings_menu.add_command(label='Reset all', command=self.master.reset_all)
