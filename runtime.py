from root_gui import Root
from enigma import Enigma
from rotor_gui import RotorMenu
from sound_ctl import Playback

root = Root()
enigma = Enigma('UKW-B', ['III', 'II', 'I'])
rotor_menu = RotorMenu()


if __name__ == '__main__':
    root.mainloop()
