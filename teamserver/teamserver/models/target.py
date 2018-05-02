"""
This module defines the Target object.
"""
from mongoengine import StringField

from ..config import COLLECTION_TARGETS
from .model import Model

class Target(Model):
    """
    This object models a target system. It stores facts about the system, any sessions, as well as
    additional settings like groups. It's status is represented as the best status of all sessions
    associated with this target.
    """
    meta = {
        'collection': COLLECTION_TARGETS,
        'indexes': [
            {
                'fields': ['name'],
                'unique': True
            },
            {
                'fields': ['uuid'],
                'unique': True
            }
        ]
    }
    name = StringField(required=True, unique=True, null=False)
    uuid = StringField(required=True, unique=True, null=False)
