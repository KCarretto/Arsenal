"""
This module contains query objects for the API.
"""
import graphene

from graphene_mongo import MongoengineConnectionField

from teamserver import models

from .mutations import get_create, get_delete, get_update

from .objects import Target, Session, SessionConfig

from .arguments import (
    CreateTargetArgs,
    DeleteTargetArgs,
    UpdateTargetArgs,

    CreateSessionArgs,
)


TYPES = [Target, Session, SessionConfig]


class Query(graphene.ObjectType):
    """
    Represents the root of GraphQL queries.
    """
    all_targets = MongoengineConnectionField(Target)
    all_sessions = MongoengineConnectionField(Session)

class Mutation(graphene.ObjectType):
    """
    Represents all possible data mutations.
    """
    create_target = get_create(Target, CreateTargetArgs).Field()
    update_target = get_update(
        Target,
        UpdateTargetArgs,
        lambda **kwargs: models.Target.objects.get(name=kwargs['name'])).Field()
    delete_target = get_delete(Target, DeleteTargetArgs).Field()

    create_session = get_create(Session, CreateSessionArgs).Field()

