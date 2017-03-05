from glob import glob
from os import path
from os import remove
from re import sub
from tkinter import *
from webbrowser import open as open_browser
from winsound import PlaySound, SND_ASYNC
from enigma.components import alphabet, EnigmaFactory


# MISC

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


class Base:
    """Base initiation class for Tk and TopLevel derivatives"""
    def __init__(self, icon:str, wm_title:str):
        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        self.resizable(False, False)
        self.iconbitmap(path.join('icons', icon))
        self.wm_title(wm_title)
        self.grab_set()


# ROOT

class Root(Tk, Base):
    """Root GUI class with enigma entry field, plugboard button, rotor button"""
    def __init__(self, enigma_cfg, cfg, bg, font, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Base.__init__(self, 'enigma.ico', enigma_cfg['model'])

        self.enigma_factory = EnigmaFactory(['enigma', 'historical_data.xml'])
        self.enigma = self.enigma_factory.produce(**enigma_cfg, master=self)
        self.playback = Playback(self)
        self.root_menu = None
        self.cfg = cfg
        self.bg = bg
        self.font = font
        self.enigma_cfg = enigma_cfg

        # Settings vars
        self._sound_enabled = IntVar()
        self._autorotate = IntVar()
        self._rotor_lock = IntVar()
        self._sync_scroll = IntVar()

        # Frames
        self.rotor_container = Frame(self, bd=1, relief='raised', bg=bg)

        # Lid
        Button(self.rotor_container, text='\n'.join('Rotors'),
               command=self.rotor_menu).pack(side='right', pady=5, padx=(15, 4))

        # Plugboard
        self.open_plugboard = Button(self, text='Plugboard',
                                     command=self.plugboard_menu)

        # Plugboard init
        self.open_plugboard.pack(side='bottom', fill='both', padx=3, pady=3)

        # Lid init
        self.rowconfigure(index=0, weight=1)

        # Container init
        self.io_board = IOBoard(self.enigma, self, self, self.playback, self.font)
        self.lightboard = Lightboard(self, self.enigma.layout, self.bg)
        self.indicator_board = IndicatorBoard(self.enigma, self.rotor_container, self.playback, self.bg, self.font)

        self.indicator_board.pack()
        self.rotor_container.pack(fill='both', padx=5, pady=5, side='top')
        self.lightboard.pack(side='top', fill='both', padx=5)
        self.io_board.pack(side='top')

        self.__make_root_menu()

        self.reset_all()

    def __reset_setting_vars(self):
        var_config = self.cfg.find(['globals', 'setting_vars'])
        self._autorotate.set(var_config['autorotate'])
        self._sound_enabled.set(var_config['sound_enabled'])
        self._sync_scroll.set(var_config['sync_scroll'])
        self._rotor_lock.set(var_config['rotor_lock'])

    @property
    def rotor_lock(self):
        return self._rotor_lock.get()

    @property
    def sound_enabled(self):
        return self._sound_enabled.get()

    def reset_all(self):  # A bit too long?
        """Sets all settings to default"""
        self.enigma.reflector = self.enigma_cfg['reflector']
        self.enigma.rotors = self.enigma_cfg['rotors']
        self.enigma.plugboard = []
        self.io_board.text_input.delete('0.0', 'end')

        self.__reset_setting_vars()

        self.update_indicators()
        self.lightboard.light_up('')
        self.io_board.format_entries()
        self.io_board.last_len = 0

    def plugboard_menu(self):
        """Opens the plugboard GUI"""
        self.wait_window(PlugboardMenu(self.enigma, self.enigma.layout, self.enigma.labels))

    def rotor_menu(self):
        """Opens the rotor gui and applies new values after closing"""
        self.wait_window(RotorMenu(self.enigma, self.bg))
        self.io_board.text_input.delete('0.0', 'end')
        self.io_board.format_entries()
        self.update_indicators()
        self.lightboard.light_up('')

    def __make_root_menu(self):
        self.root_menu = Menu(self, tearoff=0)
        settings_menu = Menu(self.root_menu, tearoff=0)
        self.root_menu.add_cascade(label='Settings', menu=settings_menu)
        self.root_menu.add_command(label='About', command=lambda: open_browser(
            'https://github.com/cernyd/enigma'))
        self.root_menu.add_command(label='Help')
        config_menu = Menu(settings_menu, tearoff=0)

        config_menu.add_command(label='Save Configuration',
                                command=self.save_config)
        config_menu.add_command(label='Load Configuration',
                                command=self.load_config)
        config_menu.add_command(label='Delete Configuration',
                                command=lambda: remove('settings.txt'))

        settings_menu.add_cascade(label='Saving and Loading', menu=config_menu)

        settings_menu.add_separator()
        settings_menu.add_checkbutton(label='Enable sound', onvalue=1,
                                      offvalue=0,
                                      variable=self._sound_enabled)
        settings_menu.add_checkbutton(label='Autorotate',
                                      variable=self._autorotate)
        settings_menu.add_checkbutton(label='Rotor lock',
                                      variable=self._rotor_lock)
        settings_menu.add_checkbutton(label='Synchronised scrolling',
                                      variable=self._sync_scroll)
        settings_menu.add_separator()
        settings_menu.add_command(label='Reset all',
                                  command=self.reset_all)

        self.config(menu=self.root_menu)

    def update_indicators(self):
        self.indicator_board.update_indicators()

    @property
    def sync_scroll(self):
        return self._sync_scroll.get()

    @property
    def autorotate(self):
        return self._autorotate.get()

    def save_config(self):  # Not flexible
        """
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
        """

    def load_config(self):  # Not flexible
        """
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
                messagebox.showerror('Loading error', f'Failed to load '
                                                      'configuration,'
                                                      'Error message:"{err}"')
        else:
            messagebox.showerror('Loading error', 'No save file found!')
        """


# PLUGBOARD MENU

class PlugboardMenu(Toplevel, Base):
    """GUI for visual plugboard pairing setup"""
    def __init__(self, enigma, layout, labels, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        Base.__init__(self, 'plugboard.ico', 'Plugboard')

        self.enigma = enigma
        self.used = []  # All used letters
        self._pairs = self.enigma.plugboard  # Pairs to return

        rows = []
        self.plug_sockets = []

        for row in layout:
            new_row = Frame(self)
            for item in row:
                self.plug_sockets.append(PlugSocket(self, new_row, self.enigma, labels[item]))
            rows.append(new_row)

        for row in rows:
            row.pack(side='top')

        for item in self.plug_sockets:
            item.pack(side='left')

        button_frame = Frame(self)

        self.apply_button = Button(button_frame, text='Apply', width=12,
                                   command=self.apply)

        self.storno_button = Button(button_frame, text='Storno', width=12,
                                    command=self.destroy)

        self.apply_button.pack(side='right', padx=5, pady=5)
        self.storno_button.pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

    def apply(self):
        self.enigma.plugboard = self.pairs
        self.destroy()

    def delete_used(self, letter):
        try:
            self.used.remove(letter)
        except ValueError:
            pass

    def add_used(self, letter):
        if letter not in self.used:
            self.used.append(letter)

    def get_target(self, label):
        for socket in self.plug_sockets:
            if socket.label == label:
                return socket

    @property
    def pairs(self):
        pairs = []
        for socket in self.plug_sockets:
            pair = [socket.label, socket.get_socket()]
            if all(pair) and pair not in pairs and list(reversed(pair)) not in pairs:
                pairs.append(pair)
        return pairs


class PlugSocket(Frame):
    """Custom made socket class"""
    def __init__(self, master, tk_master, enigma, label, *args, **kwargs):
        Frame.__init__(self, tk_master, *args, **kwargs)

        self._label = label
        self.master = master
        self.enigma = enigma
        self.pair = None

        Label(self, text=label).pack(side='top')

        self.plug_socket = PlugEntry(self, self, width=2, justify='center')

        self.plug_socket.pack(side='bottom', pady=5)

        # Loading data

        my_pair = [pair for pair in self.enigma.plugboard if
                   self.label in pair]

        if my_pair:
            my_pair = my_pair[0]
            if my_pair[0] != self.label:
                self.plug_socket.set(my_pair[0])
            else:
                self.plug_socket.set(my_pair[1])

    def link(self, target='', obj=None):  # This whole class is a mess
        if not obj:  # Link constructed locally
            if target:
                obj = self.master.get_target(target)
                if obj:
                    obj.link(obj=self)
                else:
                    return
            else:
                print('Invalid (empty) link call.')
                return
        self.plug_socket.set(obj.label)
        self.pair = obj
        self.master.add_used(self.label)

    def unlink(self, external=False):  # Attempting to unlink after each delete!
        self.master.delete_used(self.label)
        if self.pair:
            if not external:  # Would cause a loop presumably
                self.pair.unlink(True)
            self.plug_socket.clear()
            self.pair = None
        else:
            print('Invalid unlink attempt (object not linked).')

    @property
    def label(self):
        return self._label[0]

    def get_socket(self):
        return self.plug_socket.get()

    @property
    def local_forbidden(self):
        if self.label not in self.master.used:
            return [self.label] + self.master.used
        else:
            return self.master.used

    def callback(self, event_type):
        """Callback from the plug_entry widget"""
        if event_type == 'WRITE':
            self.link(self.plug_socket.get())
        elif event_type == 'DELETE':
            self.unlink()


class PlugEntry(Entry):
    def __init__(self, master, tk_master, *args, **kwargs):
        # Superclass constructor call
        self.internal_tracer = StringVar()
        Entry.__init__(self, tk_master, *args, **kwargs,
                       textvariable=self.internal_tracer)

        self.internal_tracer.trace('w', self.event)

        self.master = master
        self.last_val = ''

    def event(self, *event):
        new_val = self.validate(self.get())  # Raw new data
        delete = self.last_val and not new_val
        write = not self.last_val and new_val

        self.set(new_val)
        self.last_val = new_val

        if delete:
            self.master.callback('DELETE')
        elif write:
            self.master.callback('WRITE')

    def clear(self):
        self.delete('0', 'end')

    def set(self, string):
        self.clear()
        self.insert(0, string)

    def get(self):
        return Entry.get(self).upper()

    def validate(self, raw):
        forbidden = ''.join(self.master.local_forbidden)
        raw = sub('([\s]|[%s]|[^a-zA-Z])+' % forbidden, '', raw).upper()
        return raw[0] if raw else raw


# ROTOR MENU

class RotorMenu(Toplevel, Base):
    """GUI for setting rotor order, reflectors and ring settings"""
    def __init__(self, enigma, bg, *args, **kwargs):
        Toplevel.__init__(self, bg=bg, *args, **kwargs)
        Base.__init__(self, 'rotor.ico', 'Rotor order')

        # Enigma settings buffer
        self.enigma = enigma
        self.curr_rotors = [rotor.label for rotor in self.enigma.rotors]
        self.curr_reflector = self.enigma.reflector.label
        self.curr_ring_settings = self.enigma.ring_settings

        # Frames
        main_frame = Frame(self, bg=bg)
        button_frame = Frame(self, bg=bg)

        # Buttons
        Button(button_frame, text='Apply', width=12, command=self.apply).pack(
            side='right', padx=5, pady=5)


        Button(button_frame, text='Storno', width=12,
               command=self.destroy).pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

        # Slots for settings
        self.reflector = ReflectorSlot(self, main_frame, self.enigma.all_reflector_labels)
        self.reflector.pack(side='left', fill='y', padx=(10, 2), pady=5)

        self.rotors = [RotorSlot(self, main_frame, index, self.enigma.labels, self.enigma.all_rotor_labels) for index in range(3)]
        [rotor.pack(side='left', padx=2, pady=5, fill='y') for rotor in self.rotors]

        main_frame.pack(side='top', pady=(5, 0), padx=(0,10))

        self.update_all()

    def apply(self):
        """Applies all settings to the global enigma instance"""
        self.enigma.rotors = self.curr_rotors
        self.enigma.reflector = self.curr_reflector
        self.enigma.ring_settings = [alphabet[setting] for setting in self.curr_ring_settings]
        self.destroy()

    def update_all(self, *event):
        """Updates available radios for all slots"""
        try:
            for rotor in self.rotors:
                rotor.update_selected()
            for rotor in self.rotors:
                rotor.update_available()
        except AttributeError: # If the rotor group does not exist yet
            pass


class BaseSlot(Frame):
    def __init__(self, master, tk_master, text, *args, **kwargs):
        Frame.__init__(self, tk_master, bd=1, relief='raised', *args, **kwargs)

        Label(self, text=text, bd=1, relief='sunken').pack(side='top', padx=5,
                                                           pady=5)

        self.tk_master = tk_master
        self.master = master
        self.choice_var = StringVar()
        self.radio_group = []

        self.choice_var.trace('w', self.master.update_all)

    def generate_contents(self, contents):
        """
        :param contents: Contents to generate as tk radios
        """
        for item in contents:
            radio = Radiobutton(self, text=item, variable=self.choice_var, value=item)
            radio.pack(side='top')
            self.radio_group.append(radio)

    def update_available(self, radio_value, event=None):
        for radio in self.radio_group:
            if radio['value'] in radio_value:
                if radio['value'] != self.choice_var.get():
                    radio.config(state='disabled')
            else:
                radio.config(state='active')


class RotorSlot(BaseSlot):
    def __init__(self, master, tk_master, index, ring_labels, rotors, *args, **kwargs):
        text = ('SLOW', 'MEDIUM', 'FAST')[index] + ' ROTOR'
        BaseSlot.__init__(self, master, tk_master, text, *args, **kwargs)

        self.index = index
        self.labels = ring_labels

        self.generate_contents(rotors)

        # Ring setting indicator
        setting = self.master.enigma.ring_settings[index]

        self.ring_var = StringVar(value=ring_labels[alphabet.index(setting)])

        Label(self, text='RING\nSETTING', bd=1, relief='sunken').pack(
            side='top', fill='x', padx=4)
        OptionMenu(self, self.ring_var, *ring_labels).pack(side='top')

        self.choice_var.set(self.master.enigma.rotors[index].label)
        self.ring_var.trace('w', self.master.update_all)

    def update_selected(self, event=None):
        self.master.curr_rotors[self.index] = self.choice_var.get()
        ring_setting = self.labels.index(self.ring_var.get())
        self.master.curr_ring_settings[self.index] = ring_setting

    def update_available(self, *event):
        BaseSlot.update_available(self, radio_value=self.master.curr_rotors)


class ReflectorSlot(BaseSlot):
    def __init__(self, master, tk_master, reflectors, *args, **kwargs):
        BaseSlot.__init__(self, master, tk_master, 'REFLECTOR', *args, **kwargs)

        self.generate_contents(reflectors)
        self.choice_var.set(self.master.enigma.reflector_label)
        self.choice_var.trace('w', self.update_selected)

    def update_selected(self, *event):
        self.master.curr_reflector = self.choice_var.get()


# INDICATOR BOARD( in the main gui )

class IndicatorBoard(Frame):
    """Contains all rotor indicators"""
    def __init__(self, enigma, tk_master, playback, bg, font, *args, **kwargs):
        Frame.__init__(self, tk_master, bg=bg, *args, **kwargs)

        self.indicators = []
        for index in range(3):
            indicator = RotorIndicator(enigma, self, playback, index, bg, font)
            self.indicators.append(indicator)
            indicator.pack(side='left', fill='both', pady=10)

    def update_indicators(self):
        """Update all indicators"""
        [indicator.update_indicator() for indicator in self.indicators]


class RotorIndicator(Frame):
    """Rotor indicator for indicating or rotating a rotor"""
    def __init__(self, enigma, tk_master, playback, index, bg, font, *args, **kwargs):
        Frame.__init__(self, tk_master, bg=bg, *args, **kwargs)
        self.index = index
        self.playback = playback
        self.enigma = enigma

        cfg = dict(font=font, width=1)

        Button(self, text='+', command=lambda: self.rotate(1), **cfg).pack(
            side='top')

        self.indicator = Label(self, bd=1, relief='sunken', width=2)

        Button(self, text='-', command=lambda: self.rotate(-1), **cfg).pack(
            side='bottom')

        self.indicator.pack(side='top', pady=10, padx=20)

        self.update_indicator()

    def rotate(self, places=0):
        """Rotates the rotor with the selected index backward"""
        self.playback.play('click')
        self.enigma.rotors[self.index].rotate(places)
        self.update_indicator()

    def update_indicator(self, event=None):
        """Updates what is displayed on the indicator"""
        raw = self.enigma.rotors[self.index].position
        self.indicator.config(text=raw)


# IOBOARD

class IOBoard(Frame):
    def __init__(self, enigma, tk_master, master, playback, font, *args, **kwargs):
        Frame.__init__(self, tk_master, *args, *kwargs)
        self.enigma = enigma
        self.master = master
        self.master.bind('<Key>', self.press_event)
        self.playback = playback

        # Scrollbars
        self.input_scrollbar = Scrollbar(self, command=lambda *args: self.yview_sync(self.text_input, self.text_output, *args))
        self.output_scrollbar = Scrollbar(self, command=lambda *args: self.yview_sync(self.text_output, self.text_input, *args))

        # IO init
        Label(self, text='Input', font=font).grid(row=0, column=0)

        self.text_input = Text(self, width=25, height=5,
                               yscrollcommand=lambda *args: self.yscrollcommand_sync(self.input_scrollbar, self.output_scrollbar, *args))

        self.text_input.is_input_widget = True

        Label(self, text='Output', font=font).grid(row=2, column=0)

        self.text_output = Text(self, width=25, height=5,
                                yscrollcommand=lambda *args: self.yscrollcommand_sync(self.output_scrollbar, self.input_scrollbar, *args),
                                state='disabled')

        self.input_scrollbar.grid(row=1, column=1, sticky='ns')
        self.output_scrollbar.grid(row=3, column=1, sticky='ns')

        # IO init
        self.text_input.grid(row=1, column=0, padx=3, pady=2)
        self.text_output.grid(row=3, column=0, padx=3, pady=2)

        self.last_len = 0  # Last input string length

    def status(self):
        """Checks for any changes in the entered text length"""
        self.format_entries()
        input_length = len(self.input_box)
        if self.last_len != input_length:
            len_difference = input_length - self.last_len

            if self.last_len > input_length:
                self.last_len = input_length
                return 'shorter', len_difference
            elif self.last_len < input_length:
                self.last_len = input_length
                return 'longer', len_difference
        else:
            return False, 0

    def format_entries(self):
        """Ensures input/output fields have the same length"""
        sanitized_text = sub(r"[^A-Za-z]", '', self.input_box)
        self.input_box = sanitized_text
        self.output_box = self.output_box[:len(sanitized_text)]

    def press_event(self, event=None):
        """Activates if any key is pressed"""
        correct_widget = type(event.widget) == Text and hasattr(event.widget,
                                                                'is_input_widget')

        not_keystroke = event.state != 12 and 'Control' not in event.keysym

        if correct_widget and (not_keystroke or event.keysym in 'vVxX'):  # Because I can't trace it...
            length_status, length_difference = self.status()

            if length_status:
                if length_status == 'longer':
                    self.playback.play('button_press')
                    for letter in self.input_box[-length_difference:]:
                        self.output_box += self.enigma.button_press(letter)

                elif length_status == 'shorter' and self.master.autorotate:
                    for _ in range(abs(length_difference)):
                        self.enigma._rotate_primary(-1)

            self.master.update_indicators()

            try:
                self.master.lightboard.light_up(self.output_box[-1])
            except IndexError:
                self.master.lightboard.light_up()

    def yview_sync(self, sender, receiver, *event):
        """Sets scrollbar position if the scrollbar is dragged"""
        sender.yview(*event)
        if self.master.sync_scroll:
            receiver.yview(*event)

    def yscrollcommand_sync(self, sender, receiver, *args):
        """Sets widget view position from the yscrollcommand parameter in Text"""
        sender.set(*args)
        if self.master.sync_scroll:
            receiver.set(*args)

    @property
    def input_box(self):
        """Gets the value of the input field"""
        return self.text_input.get('0.0', 'end').upper().replace('\n', '')

    @property
    def output_box(self):
        """Gets the value of the output field"""
        return self.text_output.get('0.0', 'end').upper().replace('\n', '')

    @input_box.setter
    def input_box(self, string):
        """Sets input field to the value of string"""
        self.text_input.delete('0.0', 'end')
        self.text_input.insert('0.0', string)

    @output_box.setter
    def output_box(self, string):
        """Sets output field to the value of string"""
        self.text_output.config(state='normal')
        self.text_output.delete('0.0', 'end')
        self.text_output.insert('0.0', string)
        self.text_output.config(state='disabled')


# LIGHTBOARD

class Lightboard(Frame):
    def __init__(self, tk_master, layout, bg, *args, **kwargs):
        Frame.__init__(self, tk_master, bd=1, relief='raised', bg=bg, *args, *kwargs)

        rows = []
        self.bulbs = []

        for row in layout:
            new_row = Frame(self)
            for item in row:
                text = alphabet[item]
                self.bulbs.append(Label(new_row, text=text, font=('Arial', 14), bg=bg, padx=2))
            rows.append(new_row)

        for row in rows:
            row.pack(side='top')

        for item in self.bulbs:
            item.pack(side='left')

        self.last_bulb = None

    def light_up(self, letter=''):
        if self.last_bulb:
            self.last_bulb.config(fg='black')
        if letter:
            for bulb in self.bulbs:
                if bulb['text'] == letter:
                    bulb.config(fg='yellow')
                    self.last_bulb = bulb
                    break
