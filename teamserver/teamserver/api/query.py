"""
This module contains query objects for the API.
"""
import graphene

from graphene_mongo import MongoengineConnectionField

from .target import Target, CreateTarget
from .session import Session, CreateSession

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
    create_session = CreateSession.Field()
    create_target = CreateTarget.Field()

