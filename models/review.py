#!/usr/bin/python3
"""Review Module contains User Reviews"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review Class
    Attributes:
        place_id (str): The UUID of the Place the Review belongs to
        user_id (str): The UUID of the User that made the review
        text (str): The message the User wrote about the Place
    """
    place_id = ''
    user_id = ''
    text = ''
