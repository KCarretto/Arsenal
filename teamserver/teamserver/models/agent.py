"""
    This module defines a python object model for the Log document
    in the backend MongoDB database.
"""
from mongoengine import Document
from mongoengine.fields import ListField, StringField, IntField

from ..config import MAX_STR_LEN, COLLECTION_AGENTS

class Agent(Document):
    """
    This class represents an Agent.
    It defines what action types may be sent to this agent version.
    """
    meta = {
        'collection': COLLECTION_AGENTS,
        'indexes': [
            {
                'fields': ['agent_version'],
                'unique': True
            }
        ]
    }
    agent_version = StringField(required=True, null=False, unique=True, max_length=MAX_STR_LEN)
    supported_actions = ListField(IntField(required=True, null=False), required=True, null=False)

    @staticmethod
    def get_by_version(agent_version):
        """
        Query for an Agent by version.
        """
        return Agent.objects().get(agent_version=agent_version) # pylint: disable=no-member

    @staticmethod
    def list_agents():
        """
        Return a list of agents
        """
        return Agent.objects() # pylint: disable=no-member

    @property
    def document(self):
        """
        This property filters and returns the JSON information for a queried agent.
        """
        return {
            'agent_version': self.agent_version,
            'supported_actions': self.supported_actions,
        }

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        self.delete()
