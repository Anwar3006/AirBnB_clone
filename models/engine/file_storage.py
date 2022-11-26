#!/usr/bin/python3
"""File Storage Module
This module is in charge of the storage of the
classes and their management."""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import path


class FileStorage:
    """Represents a class that serializes instances to a JSON file
    and deserializes JSON file to instances

    Args:
        __file_path (str): path to the JSON file (ex: file.json)
        __object (dictionary): store all objects by <class name>.id
        eg BaseModel.12121212"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file """

        dictionary = {}
        for key in self.__objects:
            dictionary[key] = self.__objects[key].to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(dictionary, f)

    def reload(self):
        """Deserializes the JSON file in `__file_path` class attribute
        If the file on `__file_path` class attribute exists, each object
        on the file will be deserialized and appended to the `__objects`
        class attribute like an instance with the object data.
        """
        if path.exists(self.__file_path):
            with open(self.__file_path, mode='r', encoding='utf-8') as f:
                for o in json.load(f).values():
                    name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(name)(**o))
