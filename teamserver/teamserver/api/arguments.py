"""
This module defines arguments required for mutations.
"""
import graphene

##
### Target CRUD Args
##

class CreateTargetArgs:
    """
    Arguments used to create a target.
    """
    name = graphene.String(required=True)
    uuid = graphene.String(required=True)

class UpdateTargetArgs:
    """
    Arguments used to update a target.
    """
    name = graphene.String(required=True)
    uuid = graphene.String(required=True)

class DeleteTargetArgs:
    """
    Arguments used to delete a target.
    """
    name = graphene.String(required=True)


##
### Session CRUD Args
##

class SessionConfigInput(graphene.InputObjectType):
    """
    Defines allowed to populate a session config.
    """
    interval = graphene.Int(required=True)
    delta = graphene.Int(required=True)
    servers = graphene.List(graphene.String, required=True)

class CreateSessionArgs:
    """
    Arguments used to create a session.
    """
    target_name = graphene.String(required=True)
    config = SessionConfigInput(required=True)
    agent_version = graphene.String()
