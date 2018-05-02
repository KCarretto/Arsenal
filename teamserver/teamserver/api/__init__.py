"""
This package represents a GraphQL API for each object model in the database.
"""
import graphene

from .target import Target
from .session import Session, SessionConfig
from .query import Query, Mutation

SCHEMA = graphene.Schema(query=Query, mutation=Mutation, types=[Target, Session, SessionConfig])
