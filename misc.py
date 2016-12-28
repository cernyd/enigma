from os import path


font = ('Arial', 10)


bg = 'gray85'


def get_icon(icon):
    """Gets icon path from the icon folder"""
    return path.join('icons', icon)


def baseinit(self):
    # Load smoothness upgrade
    self.attributes("-alpha", 0.0)
    self.after(0, self.attributes, "-alpha", 1.0)
    self.resizable(False, False)
    self.grab_set()
