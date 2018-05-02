"""
This module contains the base model class.
"""

from mongoengine import Document

class Model(Document):
    """
    This class is an abstract type for models to inherit from.
    """
    meta = {
        'abstract': True
    }
