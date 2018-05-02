"""
This package represents a GraphQL API for each object model in the database.
"""
import graphene

from .schema import Target, Session, SessionConfig
from .query import Query

SCHEMA = graphene.Schema(query=Query, types=[Target, Session, SessionConfig])
