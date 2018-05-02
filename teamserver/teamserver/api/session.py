"""
This module contains the schema for Session objects.
"""
import time
import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType

from teamserver import models

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

class SessionConfigInput(graphene.InputObjectType):
    """
    Input format for the SessionConfig embedded object model.
    """
    interval = graphene.Int(required=True)
    delta = graphene.Int(required=True)
    servers = graphene.List(graphene.String)

class CreateSession(graphene.Mutation):
    """
    Create a session object model.
    """
    class Arguments:
        """
        Accepted arguments.
        """
        session_id = graphene.String(required=True)
        target_name = graphene.String(required=True)
        config = SessionConfigInput(required=True)

    session = graphene.Field(Session)

    def mutate(self, _, session_id, target_name, config, **kwargs):
        """
        Create a new session object model.
        """
        session = models.Session(
            session_id=session_id,
            target_name=target_name,
            timestamp=time.time(),
            agent_version=kwargs.get('agent_version'),
            config=models.SessionConfig(
                config.interval,
                config.delta,
                config.servers
            )
        )
        session.save(force_insert=True)

        return CreateSession(session=session)
