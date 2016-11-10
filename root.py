from tkinter import Tk, Frame, Label, Button, Text
from os import path
from enigma import Enigma
from historical import Enigma1
from rotor import Rotor
from re import sub


alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
font = ('Arial', 10)


def get_icon(icon):
    return path.join('icons', icon)


class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        # Load smoothness upgrade ^

        # Window config
        self.iconbitmap(get_icon('enigma.ico'))  # Git push and add new files ( including icons! )
        self.resizable(False, False)
        self.wm_title("Enigma")

        # Keybinds
        #self.bind('<Control-h>', None)
        #self.bind('<Control-l>', None)
        self.bind('<Key>', self.press_event)
        #self.bind('<Return>', None)

        # Frames
        self.rotor_container = Frame(self, bd=1, relief='raised', bg='gray85')
        self.io_container = Frame(self)
        self.plugboard = Frame(self)

        # Rotor widgets
        self.left_indicator = Label(self.rotor_container, text='01', bd=1, relief='sunken', width=2)
        self.mid_indicator = Label(self.rotor_container, text='01',  bd=1, relief='sunken', width=2)
        self.right_indicator = Label(self.rotor_container, text='01',  bd=1, relief='sunken', width=2)

        self.left_plus = Button(self.rotor_container, text='+', command= lambda: self.rotate_forward(2), font=font)
        self.mid_plus = Button(self.rotor_container, text='+', command= lambda: self.rotate_forward(1), font=font)
        self.right_plus = Button(self.rotor_container, text='+', command= lambda: self.rotate_forward(0), font=font)

        self.left_minus = Button(self.rotor_container, text='-', command= lambda: self.rotate_backward(2), font=font)
        self.mid_minus = Button(self.rotor_container, text='-', command= lambda: self.rotate_backward(1), font=font)
        self.right_minus = Button(self.rotor_container, text='-', command= lambda: self.rotate_backward(0), font=font)

        # Lid
        self.open_lid = Button(self.rotor_container, text='\n'.join('Rotors'))

        # Plugboard
        self.open_plugboard = Button(self.plugboard, text='Plugboard')

        # IO init
        Label(self.io_container, text='Input', font=('Arial', 12)).grid(row=0, column=0)
        self.text_input = Text(self.io_container, width=25, height=3)
        Label(self.io_container, text='Output', font=('Arial', 12)).grid(row=2, column=0)
        self.text_output = Text(self.io_container, width=25, height=3)

        """
        Input and output must always be the same length
        Input only accepts uppercase letters
        Rotor position corresponds to message length
        """

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

        # Enigma
        rotors = Enigma1.rotors
        """
        self.enigma = Enigma(Rotor(rotors['UKW-B']),
                        [Rotor(rotors['III']), Rotor(rotors['II']),
                         Rotor(rotors['I'])])
        """
        self.enigma = Enigma(Rotor(rotors['UKW-B']),
                             [Rotor(alphabet), Rotor(alphabet),
                              Rotor(alphabet)])

    def rotate_forward(self, index, event=None):
        """Rotate a rotor forward, on button press"""
        self.enigma.rotors[index].rotate()
        self.update_rotor_pos()

    def rotate_backward(self, index, event=None):
        """Rotate a rotor backward, on button press"""
        self.enigma.rotors[index].rotate(-1)
        self.update_rotor_pos()

    def update_rotor_pos(self):
        """Updates the rotor position indicators"""
        raw = str(self.enigma.rotors[2].position + 1)
        if len(raw) != 2:
            raw = '0' + raw
        self.left_indicator.config(text=raw)

        raw = str(self.enigma.rotors[1].position + 1)
        if len(raw) != 2:
            raw = '0' + raw
        self.mid_indicator.config(text=raw)

        raw = str(self.enigma.rotors[0].position + 1)
        if len(raw) != 2:
            raw = '0' + raw
        self.right_indicator.config(text=raw)

    def press_event(self, event):
        """If any text is written"""
        input_str = self.text_input.get('0.0', 'end')

        # Deleting unvalid symbols
        self.text_input.delete('0.0', 'end')
        self.text_input.insert('0.0', sub(r"[^A-Za-z]", '', input_str).upper())

        input_text = self.text_input.get('0.0', 'end')
        self.text_output.insert('end', self.enigma.button_press(input_text[-2]))
        self.update_rotor_pos()


test = Root()
test.mainloop()
