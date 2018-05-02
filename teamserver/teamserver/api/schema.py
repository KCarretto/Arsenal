"""
This module contains important schema information for each object model in the database.
"""
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType

from teamserver import models

class Target(MongoengineObjectType):
    """
    This class represents the schema for a Target object.
    """
    class Meta:
        """
        Allow access to the model.
        """
        model = models.Target
        interfaces = (Node,)

class SessionConfig(MongoengineObjectType):
    """
    This class represents the schema for a Session Config object.
    """
    class Meta:
        """
        Allow access to the model.
        """
        model = models.SessionConfig
        interfaces = (Node,)

class Session(MongoengineObjectType):
    """
    This class represents the schema for a Session object.
    """
    class Meta:
        """
        Allow access to the model.
        """
        model = models.Session
        interfaces = (Node,)
