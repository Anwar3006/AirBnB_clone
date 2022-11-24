#!/usr/bin/python3
"""City Module contains attributes to be assigned to cities"""

from models.base_model import BaseModel

class City(BaseModel):
    """City class

    Attributes:
        state_id (str): The UUID of the State the City belongs to
        name (str): The City name"""

    state_id = ''
    name = ''
