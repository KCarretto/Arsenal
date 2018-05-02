"""
This module contains the schema for Target objects.
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
