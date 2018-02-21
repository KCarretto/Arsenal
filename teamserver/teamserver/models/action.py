"""
    This module defines a python object model for the Action document
    in the backend MongoDB database.
"""

from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine.fields import StringField, FloatField, BooleanField, EmbeddedDocumentField

from .session import Session

from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN, ACTION_STATUSES, SESSION_STATUSES
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
            {
                'fields': ['target_name']
            },
            {
                'fields': ['session_id']
            },
        ]
    }
    action_id = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    target_name = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    session_id = StringField(max_length=MAX_STR_LEN)
    bound_session_id = StringField(max_length=MAX_STR_LEN)
    response = EmbeddedDocumentField(Response)

    @property
    def session(self):
        """
        This property queries for the associated session object.
        """
        return Session.objects(session_id=self.session_id) #pylint: disable=no-member

    @property
    def status(self):
        """
        This property returns the current status of the action based
        on the status of it's assigned session, as well as if it has
        been retrieved or contains a response.
        """
        # Return queued if no session has been assigned
        if self.session_id is None:
            return ACTION_STATUSES.get('queued', 'queued')
        # Return complete if we have received a response
        elif self.response is not None:
            return ACTION_STATUSES.get('complete', 'complete')

        # TODO: Raise an error if the session does not exist

        session_status = self.session.status

        if session_status == SESSION_STATUSES.get('active', 'active'):
            return ACTION_STATUSES.get('sent', 'sent')

        if session_status == SESSION_STATUSES.get('missing', 'missing'):
            return ACTION_STATUSES.get('failing', 'failing')

        return ACTION_STATUSES.get('failed', 'failed')
