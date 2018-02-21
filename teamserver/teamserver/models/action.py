"""
    This module defines a python object model for the Action document
    in the backend MongoDB database.
"""

from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine.fields import StringField, FloatField, BooleanField
from ..config import MAX_BIGSTR_LEN
from ..config import COLLECTION_ACTIONS

class Response(EmbeddedDocument):
    """
    This class represents a response from an action.

        stdout: Any output the action genereated.
        stderr: Any error messages the action generated.
        start_time: The local system time that the action started.
        end_time: The local system time that the action completed.
        error: A boolean representing if the action encountered an error.
    """

    stdout = StringField(required=True, max_length=MAX_BIGSTR_LEN)
    stderr = StringField(required=True, max_length=MAX_BIGSTR_LEN)
    start_time = FloatField(required=True, null=False)
    end_time = FloatField(required=True, null=False)
    error = BooleanField(default=True)

class Action(DynamicDocument):
    """
    This class represents an action, which is assigned to a target
    and then sent to a session. It's status is based on the status of
    the session it was sent to, as well as if the session has sent or
    responded to the action yet.
    """

    meta = {
        'collection': COLLECTION_ACTIONS,
        'indexes': [
            {
                'fields': ['action_id'],
                'unique': True
            },
        ]
    }



