from re import sub
from tkinter import Tk, Frame, Label, Button, Text, IntVar, Menu, Scrollbar
from webbrowser import open as open_browser

from enigma import Enigma
from misc import get_icon, Enigma1
from plugboard_gui import PlugboardMenu
from rotor_gui import RotorMenu
from sound_ctl import Playback
from rotor_indicator import RotorIndicator

font = ('Arial', 10)


class Root(Tk):
    """Root GUI class with enigma entry field, plugboard button, rotor button"""
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.enigma = Enigma(self, 'UKW-B', ['III', 'II', 'I'])
        self.playback = Playback(self)
        self.last_bulb = None

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Window config
        self.iconbitmap(get_icon('enigma.ico'))
        self.resizable(False, False)
        self.wm_title("Enigma")

        # Keybinds
        self.bind('<Key>', self.press_event)

        # Frames
        self.rotor_container = Frame(self, bd=1, relief='raised', bg='gray85')
        self.plugboard = Frame(self)

        # Lid
        self.open_lid = Button(self.rotor_container, text='\n'.join('Rotors'),
                               command=self.rotor_menu)

        # Plugboard
        self.open_plugboard = Button(self.plugboard, text='Plugboard', command=self.plugboard_menu)

        # Rotor
        self.left_indicator = RotorIndicator(self.rotor_container, self.enigma, self.playback, 2)
        self.mid_indicator = RotorIndicator(self.rotor_container, self.enigma, self.playback, 1)
        self.right_indicator = RotorIndicator(self.rotor_container, self.enigma, self.playback, 0)

        self.left_indicator.pack(side='left')
        self.mid_indicator.pack(side='left')
        self.right_indicator.pack(side='left')

        # Settings vars
        self._sound_enabled = IntVar()
        self._sound_enabled.set(1)
        self._autorotate = IntVar()
        self._autorotate.set(1)
        self._rotor_lock = IntVar()
        self._rotor_lock.set(0)
        self._sync_scroll = IntVar()
        self._sync_scroll.set(1)

        self.root_menu = Menu(self)
        self.settings_menu = Menu(self.root_menu, tearoff=0)
        self.root_menu.add_cascade(label='Settings', menu=self.settings_menu)
        self.root_menu.add_command(label='About', command=lambda: open_browser('https://github.com/cernyd/enigma'))
        self.root_menu.add_command(label='Help')

        self.settings_menu.add_checkbutton(label='Enable sound', onvalue=1, offvalue=0, variable=self._sound_enabled)
        self.settings_menu.add_checkbutton(label='Autorotate', variable=self._autorotate)
        self.settings_menu.add_checkbutton(label='Rotor lock', variable=self._rotor_lock)
        self.settings_menu.add_checkbutton(label='Synchronised scrolling', variable=self._sync_scroll)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label='Reset all', command=self.reset_all)

        self.config(menu=self.root_menu)

        # Plugboard init
        self.open_plugboard.pack(fill='x')

        # Lid init
        self.rowconfigure(index=0, weight=1)
        self.open_lid.pack(side='right', pady=5, padx=(15, 4))

        # Container init
        self.rotor_container.pack(fill='both', padx=5, pady=5, side='top')
        self.construct_lightboard()
        self.construct_io()
        self.plugboard.pack(side='bottom', fill='both', padx=3, pady=3)

        self.last_len = 0  # Last input string length

    def light_up(self, letter):
        if self.last_bulb:
            self.last_bulb.config(fg='black')
        for bulb in self.bulbs:
            if bulb['text'] == letter:
                bulb.config(fg='yellow')
                self.last_bulb = bulb
                break

    def construct_lightboard(self):
        self.lightboard = Frame(self, bd=1, relief='raised', bg='gray85')

        rows = []
        self.bulbs = []

        for row in Enigma1.layout:
            new_row = Frame(self.lightboard)
            for item in row:
                text = Enigma1.labels[item][0]
                self.bulbs.append(Label(new_row, text=text, font=('Arial', 14), bg='gray85'))
            rows.append(new_row)

        for row in rows:
            row.pack(side='top')

        for item in self.bulbs:
            item.pack(side='left')

        self.lightboard.pack(side='top', fill='both', padx=5)

    def construct_io(self):
        """Constructs the IO Frame widgets"""
        self.io_container = Frame(self)

        # Scrollbars
        self.input_scrollbar = Scrollbar(self.io_container)
        self.output_scrollbar = Scrollbar(self.io_container)

        # IO init
        Label(self.io_container, text='Input', font=('Arial', 12)).grid(row=0,
                                                                        column=0)

        self.text_input = Text(self.io_container, width=25, height=5,
                               yscrollcommand=self.input_scrollbar_wrapper)

        self.text_input.is_input_widget = True

        Label(self.io_container, text='Output', font=('Arial', 12)).grid(row=2,
                                                                         column=0)

        self.text_output = Text(self.io_container, width=25, height=5,
                                yscrollcommand=self.output_scrollbar_wrapper,
                                state='disabled')

        self.input_scrollbar.config(command=self.input_yview)
        self.output_scrollbar.config(command=self.output_yview)

        self.input_scrollbar.grid(row=1, column=1, sticky='ns')
        self.output_scrollbar.grid(row=3, column=1, sticky='ns')

        # IO init
        self.text_input.grid(row=1, column=0, padx=3, pady=2)
        self.text_output.grid(row=3, column=0, padx=3, pady=2)
        # self.clear_io()
        self.io_container.pack(side='top')

    def clear_io(self):
        """Clears the IO frame"""
        for obj in self.io_container.winfo_children():
            obj.destroy()

    def input_yview(self, *event):
        """Input yview controller, used to synchronise scrolling"""
        self.text_input.yview(*event)
        if self.sync_scroll:
            self.text_output.yview(*event)

    def input_scrollbar_wrapper(self, *args):
        """Relays the scrollbar set actions, used for synchronised scrolling"""
        self.input_scrollbar.set(*args)
        if self.sync_scroll:
            self.output_scrollbar.set(*args)

    def output_yview(self, *event):
        """Output yview controller, used to synchronise scrolling"""
        self.text_output.yview(*event)
        if self.sync_scroll:
            self.text_input.yview(*event)

    def output_scrollbar_wrapper(self, *args):
        """Relays the scrollbar set actions, used for synchronised scrolling"""
        self.output_scrollbar.set(*args)
        if self.sync_scroll:
            self.input_scrollbar.set(*args)

    @property
    def rotor_lock(self):
        return self._rotor_lock.get()

    @property
    def sound_enabled(self):
        return self._sound_enabled.get()

    def reset_all(self):
        """Sets all settings to default"""
        self.enigma.reflector = 'UKW-B'
        self.enigma.rotors = ['III', 'II', 'I']
        self.enigma.plugboard = []
        self.text_input.delete('0.0', 'end')
        self.last_len = 0

        self._autorotate.set(1)
        self._sound_enabled.set(1)
        self._sync_scroll.set(1)
        self._rotor_lock.set(0)

        self.left_indicator.update_indicator()
        self.mid_indicator.update_indicator()
        self.right_indicator.update_indicator()

        self.format_entries()

    def plugboard_menu(self):
        """Opens the plugboard GUI"""
        my_plugboard_menu = PlugboardMenu(self.enigma)
        self.wait_window(my_plugboard_menu)

    def rotor_menu(self):
        """Opens the rotor gui and applies new values after closing"""
        my_rotor_menu = RotorMenu(self.enigma)
        self.wait_window(my_rotor_menu)
        self.text_input.delete('0.0', 'end')
        self.format_entries()

    def button_press(self, letter):
        """Returns the encrypted letter, plays sound if sound enabled"""
        self.playback.play('button_press')
        return self.enigma.button_press(letter)

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

    @property
    def sync_scroll(self):
        return self._sync_scroll.get()

    @property
    def autorotate(self):
        return self._autorotate.get()

    def current_status(self):
        """Checks for any changes in the entered text length"""
        self.format_entries()
        input_length = len(self.input_box)
        if self.last_len != input_length:
            if self.last_len > input_length:
                self.last_len = input_length
                return 'shorter'
            elif self.last_len < input_length:
                self.last_len = input_length
                return 'longer'
        else:
            return False

    def format_entries(self):
        """Ensures input/output fields have the same length"""
        sanitized_text = sub(r"[^A-Za-z]", '', self.input_box)
        self.input_box = sanitized_text
        self.output_box = self.output_box[:len(sanitized_text)]

    def press_event(self, event=None):
        """Activates if any key is pressed"""
        correct_widget = type(event.widget) == Text and \
                         hasattr(event.widget, 'is_input_widget')
        not_keystroke = event.state != 12 and 'Control' not in event.keysym

        if correct_widget and not_keystroke:  # Because I can't trace it...
            length_status = self.current_status()

            if length_status:
                self.format_entries()
                if length_status == 'longer':
                    letter = self.button_press(self.input_box[-1])
                    output_text = self.output_box + letter
                    self.output_box = output_text
                elif length_status == 'shorter' and self.autorotate:
                    self.enigma.rotate_primary(-1)

            self.left_indicator.update_indicator()
            self.mid_indicator.update_indicator()
            self.right_indicator.update_indicator()

        if len(self.output_box):
            self.light_up(self.output_box[-1])
        else:
            self.light_up('')