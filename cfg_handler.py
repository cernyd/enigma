#!/usr/bin/env python3
"""
Copyright (C) 2016, 2017  David Cerny

This file is part of gnunigma

Gnunigma is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import xml.etree.ElementTree as ET
import yaml
from functools import wraps
from re import findall
from os import path
from copy import copy


class Config:
    """YAML configuration parser and manager"""
    def __init__(self, buffer_path):
        if type(buffer_path) == str:
            self.buffer_path = buffer_path
        else:
            self.buffer_path = path.join(*buffer_path)
        with open(self.buffer_path, 'r') as file:
            self.data = yaml.safe_load(file)

    def write(self):
        """Writes changes to the config file."""
        with open(self.buffer_path, 'w') as file:
            yaml.safe_dump(self.data, file)


class XMLConfig:
    """Universal XML configuration parser and manager"""
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
        def wrapper(self, target_path, *args, **kwargs):
            if target_path in self.__contexts:
                target_path = self.__contexts[target_path]

            return func(self, target_path, *args, **kwargs)

        return wrapper

    def __compose_path(func):
        """Converts to valid path if path list is passed"""
        @wraps(func)
        def wrapper(self, target_path, *args, **kwargs):
            if type(target_path) == list:
                target_path = ".//" + '/'.join(target_path)
            return func(self, target_path, *args, **kwargs)
        return wrapper

    @property
    def buffer(self):
        """Returns a buffer object"""
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
                err.message = """Invalid type conversion request, value
                              \"{}\" can't be converted to int!\n
                              Attribute dump > {}\n
                              All conversion requests > {}
                              """.format(value, attribs, toint)
                raise

        return attribs

    @staticmethod
    def __process_data(element, data_type='ATTRS'):
        """Returns data appropriate to the requested type."""
        if data_type == 'SUBTAGS':
            return [item.tag for item in element]
        elif data_type == 'SUBATTRS':
            subattrs = []
            for item in element:
                subattrs.append(XMLConfig.__process_attribs(copy(item.attrib)))
            return subattrs
        elif data_type == 'TEXT':
            return element.text
        elif data_type == 'ATTRS':
            return XMLConfig.__process_attribs(copy(element.attrib))
        elif data_type == 'TAG':
            return element.tag
        elif data_type == 'OBJ':
            return element
        else:
            raise ValueError("Invalid data type \"{}\"!".format(data_type))

    def clear_focus(self):
        """Clears current buffer focus"""
        self.__curr_focus = ''

    @__compose_path
    def focus_buffer(self, data_path):
        """Sets the buffer to only a part of the original one."""
        self.__curr_focus = data_path

    @__compose_path
    def new_context(self, context_path, name):
        """Creates a new shortcut ( can be then accessed
        in the get_data method )"""
        self.__contexts[name] = context_path

    @__compose_path
    @__check_context
    def find(self, data_path, data_type='ATTRS'):
        """Returns data based on data type and data path specified"""
        data = self.buffer.find(data_path)
        assert data is not None, "No data found for path \"{}\"!".format(data_path)

        return XMLConfig.__process_data(data, data_type)

    @__compose_path
    @__check_context
    def iter_find(self, data_path, data_type='ATTRS'):
        """Finds all data iteratively in the current buffer scope."""
        data = list(self.buffer.iter(data_path))
        assert data is not None and data != [], "No data found for path \"{}\"!".format(data_path)

        return [XMLConfig.__process_data(item, data_type) for item in data]

    def clear_children(self, target_path):
        """Clears all children of an object"""
        self.clear_focus()
        obj = self.find(target_path, 'OBJ')
        for child in obj:
            obj.remove(child)

    @__compose_path
    @__check_context
    def new_subelement(self, master_path, tag, **attrib):
        """Creates a new subelement of and existing element in the
        parsed tree"""
        self.clear_focus()
        master_obj = self.find(master_path, 'OBJ')
        ET.SubElement(master_obj, tag, attrib=attrib)

    def write(self):
        """Writes changes to the config file. Unfortunately, this makes the xml
        save look bad because it does not split to new line."""
        self.tree.write(self.buffer_path)
