"""
This module defines arguments required for mutations.
"""
import graphene

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

class CreateSessionArgs:
    """
    Arguments used to create a session.
    """
    target_name = graphene.String(required=True)
