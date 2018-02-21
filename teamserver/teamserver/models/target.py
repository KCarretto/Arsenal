"""
    This module defines a python object model for the Target document
    in the backend MongoDB database.
"""

from mongoengine import DynamicDocument
from mongoengine.fields import StringField, DictField, ListField

from ..config import MAX_STR_LEN
from ..config import COLLECTION_TARGETS

class Target(DynamicDocument):
    """
    This class represents a target system. It stores facts about the
    system, any sessions, as well as additional settings like groups.
    It's status is represented as the best status of all sessions
    associated with this target.
    """

    meta = {
        'collection': COLLECTION_TARGETS,
        'indexes': [
            {
                'fields': ['target_id'],
                'unique': True
            },
        ]
    }

    name = StringField(required=True, null=False, max_length=MAX_STR_LEN, unique=True)
    facts = DictField(required=True, null=False)
    group_tags = ListField(StringField(null=False, max_length=MAX_STR_LEN))
    sessions = ListField(StringField(null=False, max_length=MAX_STR_LEN))


