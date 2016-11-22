from os import path
from re import sub
from tkinter import Tk, Frame, Label, Button, Text, IntVar, Menu

from plugboard_gui import PlugboardMenu
from enigma import Enigma
from rotor_gui import RotorMenu
from sound_ctl import Playback

from webbrowser import open as open_browser

font = ('Arial', 10)


def get_icon(icon):
    return path.join('icons', icon)


def format_digit(number):
    if len(number) != 2:
        number = '0' + number
    return number


class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Window config
        self.iconbitmap(get_icon(
            'enigma.ico'))  # Git push and add new files ( including icons! )
        self.resizable(False, False)
        self.wm_title("Enigma")

        # Keybinds
        # self.bind('<Control-h>', None)
        # self.bind('<Control-l>', None)
        self.bind('<Key>', self.press_event)
        # self.bind('<Return>', None)

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
                                command=lambda: self.rotate_forward(2),
                                font=font)
        self.mid_plus = Button(self.rotor_container, text='+',
                               command=lambda: self.rotate_forward(1),
                               font=font)
        self.right_plus = Button(self.rotor_container, text='+',
                                 command=lambda: self.rotate_forward(0),
                                 font=font)

        self.left_minus = Button(self.rotor_container, text='-',
                                 command=lambda: self.rotate_backward(2),
                                 font=font)
        self.mid_minus = Button(self.rotor_container, text='-',
                                command=lambda: self.rotate_backward(1),
                                font=font)
        self.right_minus = Button(self.rotor_container, text='-',
                                  command=lambda: self.rotate_backward(0),
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
        self.sound_enabled = IntVar()
        self.sound_enabled.set(1)
        self.autorotate = IntVar()
        self.autorotate.set(1)

        self.root_menu = Menu(self)
        self.settings_menu = Menu(self.root_menu, tearoff=0)
        self.root_menu.add_cascade(label='Settings', menu=self.settings_menu)
        self.root_menu.add_command(label='About', command=lambda: open_browser('https://github.com/cernyd/enigma'))
        self.root_menu.add_command(label='Help')


        self.settings_menu.add_checkbutton(label='Enable sound', onvalue=1, offvalue=0, variable=self.sound_enabled)
        self.settings_menu.add_checkbutton(label='Autorotate', variable=self.autorotate)
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

        # Enigma defaults
        self.enigma = Enigma('UKW-B', ['III', 'II', 'I'])

        self.last_len = 0  # Last input string length

    def reset_all(self):
        self.enigma.use_reflector('UKW-B')
        self.enigma.use_rotors(['III', 'II', 'I'])
        self.text_input.delete('0.0', 'end')
        self.update_rotor_pos()
        self.format_entries()

    def plugboard_menu(self):
        myPlugboardMenu = PlugboardMenu()

    def rotor_menu(self):
        myRotorMenu = RotorMenu(self.enigma.get_rotors())
        self.wait_window(myRotorMenu)
        new_values = myRotorMenu.get_rotors()
        if new_values:
            self.enigma.use_reflector(new_values[0])
            self.enigma.use_rotors(new_values[1:])
            self.text_input.delete('0.0', 'end')
            self.format_entries()
            self.update_rotor_pos()

        self.enigma.set_ring_settings(myRotorMenu.get_ring_settings())

    def button_press(self, letter):
        if self.sound_enabled.get():
            Playback.sound_enabled = self.sound_enabled.get()
            Playback.play('button_press')
        return self.enigma.button_press(letter)

    def set_input(self, string):
        self.text_input.delete('0.0', 'end')
        self.text_input.insert('0.0', string)

    def set_output(self, string):
        self.text_output.delete('0.0', 'end')
        self.text_output.insert('0.0', string)

    def get_input(self):
        return self.text_input.get('0.0', 'end').upper().replace('\n', '')

    def get_output(self):
        return self.text_output.get('0.0', 'end').upper().replace('\n', '')

    def current_status(self):
        input_length = len(self.get_input())
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
        sanitized_text = sub(r"[^A-Za-z]", '', self.get_input())
        self.set_input(sanitized_text)
        # Input trimming
        self.set_output(self.get_output()[:len(sanitized_text)])

    def rotate_forward(self, index, event=None):
        """Rotate a rotor forward, on button press"""
        Playback.sound_enabled = self.sound_enabled.get()
        Playback.play('click')
        self.enigma.rotors[index].rotate()
        self.update_rotor_pos()

    def rotate_backward(self, index, event=None):
        """Rotate a rotor backward, on button press"""
        Playback.sound_enabled = self.sound_enabled.get()
        Playback.play('click')
        self.enigma.rotors[index].rotate(-1)
        self.update_rotor_pos()

    def update_rotor_pos(self):
        """Updates the rotor position indicators"""
        raw = str(self.enigma.rotors[2].position + 1)
        self.left_indicator.config(text=format_digit(raw))

        raw = str(self.enigma.rotors[1].position + 1)
        self.mid_indicator.config(text=format_digit(raw))

        raw = str(self.enigma.rotors[0].position + 1)
        self.right_indicator.config(text=format_digit(raw))

        self.enigma.prt_positions()

    def press_event(self, event):
        """If any text is written"""
        length_status = self.current_status()

        if length_status:
            self.format_entries()
            if length_status == 'longer':
                output_text = self.get_output() + self.button_press(
                    self.get_input()[-1])
                self.set_output(output_text)
            elif length_status == 'shorter' and self.autorotate.get():
                self.enigma.rotate_primary(-1)

            self.update_rotor_pos()


test = Root()
test.mainloop()
