from tkinter import Frame, Scrollbar, Text, Label
from re import sub
from misc import font, select_all


class IOBoard(Frame):
    def __init__(self, master, enigma_instance, tk_master=None, *args, **kwargs):
        tk_master = tk_master if tk_master else master
        Frame.__init__(self, tk_master, *args, *kwargs)

        self.master = master
        self.enigma = enigma_instance

        self.master.bind('<Key>', self.press_event)

        # Scrollbars
        self.input_scrollbar = Scrollbar(self)
        self.output_scrollbar = Scrollbar(self)

        # IO init
        Label(self, text='Input', font=font).grid(row=0, column=0)

        self.text_input = Text(self, width=25, height=5,
                               yscrollcommand=self.input_scrollbar_wrapper)

        self.text_input.is_input_widget = True

        Label(self, text='Output', font=font).grid(row=2, column=0)

        self.text_output = Text(self, width=25, height=5,
                                yscrollcommand=self.output_scrollbar_wrapper,
                                state='disabled')

        self.input_scrollbar.config(command=self.input_yview)
        self.output_scrollbar.config(command=self.output_yview)

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
                return ['shorter', len_difference]
            elif self.last_len < input_length:
                self.last_len = input_length
                return ['longer', len_difference]
        else:
            return [False, 0]

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

        if correct_widget and not_keystroke:  # Because I can't trace it...
            length_status, length_difference = self.status()

            if length_status:
                self.format_entries()
                if length_status == 'longer':
                    letter = self.button_press(self.input_box[-1])
                    self.output_box = self.output_box + letter
                elif length_status == 'shorter' and self.master.autorotate:
                    self.enigma.rotate_primary(-1)

            self.master.update_indicators()

            if len(self.output_box):
                self.master.lightboard.light_up(self.output_box[-1])
            else:
                self.master.lightboard.light_up()

    def input_yview(self, *event):
        """Input yview controller, used to synchronise scrolling"""
        self.text_input.yview(*event)
        if self.master.sync_scroll:
            self.text_output.yview(*event)

    def input_scrollbar_wrapper(self, *args):
        """Relays the scrollbar set actions, used for synchronised scrolling"""
        self.input_scrollbar.set(*args)
        if self.master.sync_scroll:
            self.output_scrollbar.set(*args)

    def output_yview(self, *event):
        """Output yview controller, used to synchronise scrolling"""
        self.text_output.yview(*event)
        if self.master.sync_scroll:
            self.text_input.yview(*event)

    def output_scrollbar_wrapper(self, *args):
        """Relays the scrollbar set actions, used for synchronised scrolling"""
        self.output_scrollbar.set(*args)
        if self.master.sync_scroll:
            self.input_scrollbar.set(*args)

    @property
    def input_box(self):
        """Gets the value of the input field"""
        return self.text_input.get(*select_all).upper().replace('\n', '')

    @property
    def output_box(self):
        """Gets the value of the output field"""
        return self.text_output.get(*select_all).upper().replace('\n', '')

    @input_box.setter
    def input_box(self, string):
        """Sets input field to the value of string"""
        self.text_input.delete(*select_all)
        self.text_input.insert('0.0', string)

    @output_box.setter
    def output_box(self, string):
        """Sets output field to the value of string"""
        self.text_output.config(state='normal')
        self.text_output.delete(*select_all)
        self.text_output.insert('0.0', string)
        self.text_output.config(state='disabled')

    def button_press(self, letter):
        """Returns the encrypted letter, plays sound if sound enabled"""
        self.master.playback.play('button_press')
        return self.enigma.button_press(letter)
