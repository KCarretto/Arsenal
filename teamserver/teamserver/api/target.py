"""
This module contains the schema for Target objects.
"""
import graphene

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

class FactInput(graphene.InputObjectType):
    """
    Input format for the Facts embedded object model.
    """
    interval = graphene.Int(required=True)
    delta = graphene.Int(required=True)
    servers = graphene.List(graphene.String)

class CreateTarget(graphene.Mutation):
    """
    Create a target object model.
    """
    class Arguments:
        """
        Accepted arguments.
        """
        name = graphene.String(required=True)
        uuid = graphene.String(required=True)

    target = graphene.Field(Target)

    def mutate(self, _, name, uuid):
        """
        Create a new target object model.
        """
        target = models.Target(
            name=name,
            uuid=uuid,
        )
        target.save(force_insert=True)

        return CreateTarget(target=target)
