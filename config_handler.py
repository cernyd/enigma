import xml.etree.ElementTree as ET


class Config:
    """Handles any type of config"""
    def __init__(self, buffer_path):
        self.__config_buffer = ET.parse(buffer_path)

    def __getitem__(self, group, item):
        found = self.__config_buffer.find(group).find(item).attrib

        split_items = found.get('split', None)
        if split_items:
            for command in split_items.split():
                found[command] = found[command].split()

        return found