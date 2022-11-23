#!/usr/bin/python3
"""Defines a Base calss."""
import uuid
from datetime import datetime
import models

class BaseModel:
    """Represents all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel
        Args:
            id: unique id of each Base
            created_at: datetime during instantiation
            updated_at: datetime during update of object"""

        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    v = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
                if k != "__class__":
                    setattr(self, k, v)

        models.storage.new(self)

    def __str__(self):
        """Returns the string representation of keys/values"""

        return (str("[{}] ({}) {}".format(self.__class__.__name__,
                                          self.id,
                                          self.__dict__)))

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime"""

        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values
        of __dict__ of the instance"""

        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat
        dictionary['updated_at'] = self.updated_at.isoformat

        return dictionary
