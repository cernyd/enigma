import xml.etree.ElementTree as ET
from functools import wraps
from re import findall
from os import path


class Config:
    """Universal configuration parser and manager"""
    def __init__(self, buffer_path):
        self.__contexts = {}
        self.__curr_focus = ''
        try:
            if type(buffer_path) == list:
                buffer_path = path.join(*buffer_path)

            self.buffer_path = buffer_path
            self.tree = ET.parse(buffer_path)
            self.__buffer_data = self.tree.getroot()
        except FileNotFoundError as err:
            err.message = "Requested configuration file not found!"
            raise

    def __check_context(func):
        """Swaps the target if the address is bookmarked"""
        @wraps(func)
        def wrapper(self, path, *args, **kwargs):
            if path in self.__contexts:
                path = self.__contexts[path]

            return func(self, path, *args, **kwargs)

        return wrapper

    def __compose_path(func):
        """Converts to valid path if path list is passed"""
        @wraps(func)
        def wrapper(self, path, *args, **kwargs):
            if type(path) == list:
                path = ".//" + '/'.join(path)
            return func(self, path, *args, **kwargs)
        return wrapper

    @property
    def buffer(self):
        if self.__curr_focus:
            return self.__buffer_data.find(self.__curr_focus)
        else:
            return self.__buffer_data

    @staticmethod
    def __process_attribs(attribs: dict):
        """Splits attributes if they have the 'split' flag set."""
        to_split = attribs.pop('split', None)
        toint = attribs.pop('toint', None)

        if attribs:
            if to_split:
                for key, value in attribs.items():
                    if key in to_split or to_split == "*":
                        value = value.split()
                    attribs[key] = value

            try:
                if toint:
                    for key, value in attribs.items():
                        if key in toint or toint == "*":
                            valtype = type(value)
                            if valtype == str:
                                value = int(value)
                            elif valtype == list:
                                value = [int(item) for item in value]
                        attribs[key] = value
            except ValueError as err:
                value = findall("\'(.+)\'$", err.message)
                err.message = f"Invalid type conversion request, " \
                              f"value \"{value}\" can't be converted to int!\n" \
                              f"Attribute dump > {attribs}\n" \
                              f"All conversion requests > {toint}"
                raise

        return attribs

    @staticmethod
    def __process_data(element, data_type='ATTRS'):
        """Returns data appropriate to the requested type."""
        if data_type == 'SUBTAGS':
            return [item.tag for item in element]
        elif data_type == 'SUBATTRS':
            return [Config.__process_attribs(item.attrib) for item in element]
        elif data_type == 'TEXT':
            return element.text
        elif data_type == 'ATTRS':
            return Config.__process_attribs(element.attrib)
        elif data_type == 'TAG':
            return element.tag
        elif data_type == 'OBJ':
            return element
        else:
            raise ValueError(f"Invalid data type \"{data_type}\"!")

    def clear_focus(self):
        self.__curr_focus = ''

    @__compose_path
    def focus_buffer(self, data_path):
        """Sets the buffer to only a part of the original one."""
        self.__curr_focus = data_path

    @__compose_path
    def new_context(self, context_path, name):
        """Creates a new shortcut ( can be then accessed in the get_data method )"""
        self.__contexts[name] = context_path

    @__compose_path
    @__check_context
    def find(self, data_path, data_type='ATTRS'):
        """Returns data based on data type and data path specified"""
        data = self.buffer.find(data_path)  # Should somehow iterate over results
        err_msg = f"No data found for path \"{data_path}\"!"
        assert data != None, err_msg

        return Config.__process_data(data, data_type)

    @__compose_path
    @__check_context
    def iter_find(self, data_path, data_type='ATTRS'):
        """Finds all data iteratively in the current buffer scope."""
        data = list(self.buffer.iter(data_path))
        err_msg = f"No data found for path \"{data_path}\"!"
        assert data != None and data != [], err_msg

        return [Config.__process_data(item, data_type) for item in data]

    def save_data(self, data):
        """Saves the edited data buffer back to the original file"""
        self.clear_focus()

        save_location = self.buffer.find('saved')

        ET.SubElement(save_location, 'gui', attrib=dict(split='*', toint='*', **data['gui']))
        ET.SubElement(save_location, 'enigma', attrib=dict(split='rotors uhr_pairs normal_pairs', **data['enigma']))

        self.tree.write(self.buffer_path)
