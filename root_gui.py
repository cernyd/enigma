from re import sub
from tkinter import Tk, Frame, Label, Button, Text, IntVar, Menu
from webbrowser import open as open_browser

from enigma import Enigma
from misc import get_icon
from plugboard_gui import PlugboardMenu
from rotor_gui import RotorMenu
from sound_ctl import Playback

font = ('Arial', 10)


class Root(Tk):
    """Root GUI class with enigma entry field, plugboard button, rotor button"""
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

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
        self.io_container = Frame(self)
        self.plugboard = Frame(self)

        # Rotor widgets
        self.left_indicator = Label(self.rotor_container, text='01', bd=1,
                                    relief='sunken', width=2)
        self.mid_indicator = Label(self.rotor_container, text='01', bd=1,
                                   relief='sunken', width=2)
        self.right_indicator = Label(self.rotor_container, text='01', bd=1,
                                     relief='sunken', width=2)

        self.left_plus = Button(self.rotor_container, text='+',
                                command=lambda: self.rotate(2, 1),
                                font=font)
        self.mid_plus = Button(self.rotor_container, text='+',
                               command=lambda: self.rotate(1, 1),
                               font=font)
        self.right_plus = Button(self.rotor_container, text='+',
                                 command=lambda: self.rotate(0, 1),
                                 font=font)

        self.left_minus = Button(self.rotor_container, text='-',
                                 command=lambda: self.rotate(2, -1),
                                 font=font)
        self.mid_minus = Button(self.rotor_container, text='-',
                                command=lambda: self.rotate(1, -1),
                                font=font)
        self.right_minus = Button(self.rotor_container, text='-',
                                  command=lambda: self.rotate(0, -1),
                                  font=font)

        # Lid
        self.open_lid = Button(self.rotor_container, text='\n'.join('Rotors'),
                               command=self.rotor_menu)

        # Plugboard
        self.open_plugboard = Button(self.plugboard, text='Plugboard', command=self.plugboard_menu)

        # IO init
        Label(self.io_container, text='Input', font=('Arial', 12)).grid(row=0,
                                                                        column=0)
        self.text_input = Text(self.io_container, width=25, height=3)
        Label(self.io_container, text='Output', font=('Arial', 12)).grid(row=2,
                                                                         column=0)
        self.text_output = Text(self.io_container, width=25, height=3)

        # Rotor
        self.left_indicator.grid(row=1, column=0, sticky='we', padx=20, pady=3)
        self.mid_indicator.grid(row=1, column=1, sticky='we', padx=20, pady=3)
        self.right_indicator.grid(row=1, column=2, sticky='we', padx=20, pady=3)

        self.left_plus.grid(row=2, column=0)
        self.mid_plus.grid(row=2, column=1)
        self.right_plus.grid(row=2, column=2)

        self.left_minus.grid(row=0, column=0)
        self.mid_minus.grid(row=0, column=1)
        self.right_minus.grid(row=0, column=2)

        # Menu
        self._sound_enabled = IntVar()
        self._sound_enabled.set(1)
        self._autorotate = IntVar()
        self.autorotate = 1

        self.root_menu = Menu(self)
        self.settings_menu = Menu(self.root_menu, tearoff=0)
        self.root_menu.add_cascade(label='Settings', menu=self.settings_menu)
        self.root_menu.add_command(label='About', command=lambda: open_browser('https://github.com/cernyd/enigma'))
        self.root_menu.add_command(label='Help')


        self.settings_menu.add_checkbutton(label='Enable sound', onvalue=1, offvalue=0, variable=self._sound_enabled)
        self.settings_menu.add_checkbutton(label='Autorotate', variable=self._autorotate)
        self.settings_menu.add_checkbutton(label='Rotor lock')
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label='Reset all', command=self.reset_all)

        self.config(menu=self.root_menu)

        # Plugboard init
        self.open_plugboard.pack(fill='x')

        # Lid init
        self.rowconfigure(index=0, weight=1)
        self.open_lid.grid(column=3, row=0, rowspan=3, pady=5, padx=(15, 4))

        # IO init
        self.text_input.grid(row=1, column=0, padx=3, pady=2)
        self.text_output.grid(row=3, column=0, padx=3, pady=2)

        # Container init
        self.rotor_container.pack(fill='both', padx=5, pady=5, side='top')
        self.plugboard.pack(side='bottom', fill='both', padx=3, pady=3)
        self.io_container.pack(side='bottom')

        self.last_len = 0  # Last input string length

    def reset_all(self):
        """Sets all settings to default"""
        enigma.reflector = 'UKW-B'
        enigma.rotors = ['III', 'II', 'I']
        self.text_input.delete('0.0', 'end')
        self.update_rotor_pos()
        self.format_entries()

    def plugboard_menu(self):
        """Opens the plugboard GUI"""
        my_plugboard_menu = PlugboardMenu(enigma.plugboard)
        self.wait_window(my_plugboard_menu)
        enigma.plugboard = PlugboardMenu.return_data

    def rotor_menu(self):
        """Opens the rotor gui and applies new values after closing"""
        my_rotor_menu = RotorMenu(enigma.rotor_labels, enigma.ring_settings)
        self.wait_window(my_rotor_menu)
        new_values = my_rotor_menu.get_rotors()
        if new_values:
            enigma.reflector = new_values[0]
            enigma.rotors = new_values[1:]
            self.text_input.delete('0.0', 'end')
            self.format_entries()
            self.update_rotor_pos()

        enigma.ring_settings = my_rotor_menu.get_ring_settings()

    def button_press(self, letter):
        """Returns the encrypted letter, plays sound if sound enabled"""
        if self._sound_enabled:
            Playback.sound_enabled = self._sound_enabled
            Playback.play('button_press')
        return enigma.button_press(letter)

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
        self.text_output.delete('0.0', 'end')
        self.text_output.insert('0.0', string)

    @property
    def autorotate(self):
        return self._autorotate.get()

    @autorotate.setter
    def autorotate(self, num):
        self._autorotate.set(num)

    def current_status(self):
        """Checks for any changes in the entered text length"""
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
        length_status = self.current_status()

        if length_status:
            self.format_entries()
            if length_status == 'longer':
                output_text = self.output_box + self.button_press(self.input_box[-1])
                self.output_box = output_text
            elif length_status == 'shorter' and self.autorotate:
                enigma.rotate_primary(-1)

            self.update_rotor_pos()



def format_digit(number: int) -> str:
    """Adds returns 01 when 1 entered etc."""
    number = str(number)
    if len(number) != 2:
        number = '0' + number
    return number


class RotorIndicator(Frame):
    def __init__(self, index, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.index = index

        self.indicator = Label(self, text='01', bd=1,
                               relief='sunken', width=2)

        self.plus = Button(self, text='+', command=lambda: self.rotate(2, 1),
                           font=font)

        self.minus = Button(self, text='-', command=lambda: self.rotate(2, -1),
                            font=font)

        self.minus.pack(side='top')
        self.indicator.pack(side='top')
        self.plus.pack(side='top')

    def rotate(self, index, places=0):
        """Rotates the rotor with the selected index backward"""
        Playback.sound_enabled = sound_enabled
        Playback.play('click')
        enigma.rotors[self.index].rotate(places)
        self.update_indicator()

    def update_indicator(self):
        raw = enigma.rotors[2].position + 1
        text = format_digit(raw)
        self.indicator.config(text=text)