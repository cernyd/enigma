from glob import glob
from tkinter import Tk, Frame, Button, IntVar, messagebox

from boards.indicator_board import IndicatorBoard
from boards.io_board import IOBoard
from boards.lightboard import Lightboard
from data_handlers import save_config, load_config
from enigma_components.enigma import TkEnigma
from gui_components.plugboard_gui import PlugboardMenu
from gui_components.root_menu import RootMenu
from gui_components.rotor_gui import RotorMenu
from misc import get_icon, baseinit, bg, select_all
from sound_ctl import Playback


class Root(Tk):
    """Root GUI class with enigma entry field, plugboard button, rotor button"""
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        baseinit(self)

        self.enigma = TkEnigma(self, 'UKW-B', ['I', 'II', 'III'])
        self.playback = Playback(self)

        # Window config
        self.iconbitmap(get_icon('enigma.ico'))
        self.wm_title("Enigma")

        # Frames
        self.rotor_container = Frame(self, bd=1, relief='raised', bg=bg)

        self.indicator_board = IndicatorBoard(self.rotor_container)

        # Lid
        Button(self.rotor_container, text='\n'.join('Rotors'),
               command=self.rotor_menu).pack(side='right', pady=5, padx=(15, 4))

        # Plugboard
        self.open_plugboard = Button(self, text='Plugboard',
                                     command=self.plugboard_menu)

        # Settings vars
        self._sound_enabled = IntVar(value=1)
        self._autorotate = IntVar(value=1)
        self._rotor_lock = IntVar(value=0)
        self._sync_scroll = IntVar(value=1)

        self.config(menu=RootMenu(self))

        # Plugboard init
        self.open_plugboard.pack(side='bottom', fill='both', padx=3, pady=3)

        # Lid init
        self.rowconfigure(index=0, weight=1)

        # Container init
        self.indicator_board.pack()
        self.rotor_container.pack(fill='both', padx=5, pady=5, side='top')
        self.lightboard = Lightboard(self)
        self.lightboard.pack(side='top', fill='both', padx=5)
        self.io_board = IOBoard(self, self.enigma)
        self.io_board.pack(side='top')

    @property
    def rotor_lock(self):
        return self._rotor_lock.get()

    @property
    def sound_enabled(self):
        return self._sound_enabled.get()

    def reset_all(self):  # A bit too long?
        """Sets all settings to default"""
        self.enigma.reflector = 'UKW-B'
        self.enigma.rotors = ['III', 'II', 'I']
        self.enigma.plugboard = []
        self.io_board.text_input.delete(*select_all)
        self.last_len = 0

        self._autorotate.set(1)
        self._sound_enabled.set(1)
        self._sync_scroll.set(1)
        self._rotor_lock.set(0)

        self.update_indicators()
        self.lightboard.light_up('')
        self.io_board.format_entries()

    def plugboard_menu(self):
        """Opens the plugboard GUI"""
        self.wait_window(PlugboardMenu(self.enigma))

    def rotor_menu(self):
        """Opens the rotor gui and applies new values after closing"""
        self.wait_window(RotorMenu(self.enigma))
        self.io_board.text_input.delete(*select_all)
        self.io_board.format_entries()

    @property
    def sync_scroll(self):
        return self._sync_scroll.get()

    @property
    def autorotate(self):
        return self._autorotate.get()

    def save_config(self):  # Not flexible
        choice = True
        if glob('settings.txt'):
            msg = 'Save file detected, do you wish to overwrite with new ' \
                  'configuration data?'

            choice = messagebox.askyesno('Save file detected', msg)

        if choice:
            data = dict(root=dict(sound_enabled=self._sound_enabled.get(),
                                  autorotate=self._autorotate.get(),
                                  rotor_lock=self._rotor_lock.get(),
                                  synchronised_scrolling=self._sync_scroll.get()),
                        enigma=self.enigma.dump_config())
            save_config(data)

    def load_config(self):  # Not flexible
        if glob('settings.txt'):
            try:
                data = load_config()
                self._sound_enabled.set(data['root']['sound_enabled'])
                self._autorotate.set(data['root']['autorotate'])
                self._rotor_lock.set(data['root']['rotor_lock'])
                self._sync_scroll.set(data['root']['synchronised_scrolling'])
                self.reset_all()
                self.enigma.load_config(data['enigma'])
                self.update_indicators()
            except Exception as err:
                messagebox.showerror('Loading error', 'Failed to load '
                                                      'configuration,'
                                                      'Error message:"%s"' % err)
        else:
            messagebox.showerror('Loading error', 'No save file found!')
