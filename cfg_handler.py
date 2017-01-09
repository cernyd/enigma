import xml.etree.ElementTree as ET
from os import path


class Config:
    """Universal configuration parser and manager"""
    def __init__(self, buffer_path):
        try:
            self.__buffer = ET.parse(path.join(*buffer_path)).getroot()
        except FileNotFoundError as err:
            err.message = "Requested configuration file not found!"
            raise

        self.__contexts = {}

    @staticmethod
    def __split_attribs(attribs: dict):
        """Splits attributes if they have the 'split' flag set."""
        to_split = attribs.get('split', None)

        if to_split:
            to_split = to_split.split()
            for key, value in attribs.items():
                if key in to_split and type(value) == str:
                    value = value.split()
                attribs[key] = value

        return attribs

    @staticmethod
    def __process_data(element, data_type='ATTRS'):
        """Returns data appropriate to the requested type."""
        if data_type == 'SUBTAGS':
            return [item.tag for item in element]
        elif data_type == 'SUBATTRS':
            return [Config.__split_attribs(item.attrib) for item in element]
        elif data_type == 'TEXT':
            return element.text
        elif data_type == 'ATTRS':
            return Config.__split_attribs(element.attrib)
        elif data_type == 'TAG':
            return element.tag
        elif data_type == 'OBJ':
            return element
        else:
            raise ValueError(f"Invalid data type \"{data_type}\"!")

    @staticmethod
    def __compose_path(data_path):
        """Creates a path if the path is not joined"""
        path_type = type(data_path)
        if path_type == str:
            return data_path
        elif path_type == list:
            return ".//" + '/'.join(data_path)

    def new_context(self, name, context_path: list):
        """Creates a new 'bookmark' for accessing data easily"""
        context_path = Config.__compose_path(context_path)
        self.__contexts[name] = self.__buffer.find(context_path)

    def get_data(self, data_path, data_type='ATTRS'):
        """Returns data based on data type and data path specified"""
        data_path = Config.__compose_path(data_path)

        if data_path in self.__contexts:
            data = self.__contexts[data_path]
        else:
            data = self.__buffer.find(data_path)

        return Config.__process_data(data, data_type)

    def __getitem__(self, item):
        return self.__contexts[item]
