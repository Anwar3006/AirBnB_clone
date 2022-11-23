#!/usr/bin/python3
"""Defines a file storage class."""
import json
from models.base_model import BaseModel


class FileStorage():
    """Represents a class that serializes instances to a JSON file
    and deserializes JSON file to instances
    
    Args:
        __file_path (str): path to the JSON file (ex: file.json)
        __object (dictionary): store all objects by <class name>.id eg BaseModel.12121212"""

    __file_path = "file1.json"
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
        for key, values in self.__objects.items():
            dictionary[key] = self.__objects[key].to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(dictionary))

    def reload(self):
        """Deserializes the JSON file to __objects"""

        try:
            with open(self.__file_path, "r", encoding="utf-8")as f:
                json.loads(f)
        except FileNotFoundError:
            pass
