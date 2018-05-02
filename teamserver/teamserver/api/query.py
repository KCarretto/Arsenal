"""
This module contains query objects for the API.
"""
import graphene

from graphene_mongo import MongoengineConnectionField

from .schema import Target, Session

class Query(graphene.ObjectType):
    """
    Represents a basic graphql query.
    """
    all_targets = MongoengineConnectionField(Target)
    all_sessions = MongoengineConnectionField(Session)
