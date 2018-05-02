"""
This package represents a GraphQL API for each object model in the database.
"""
import graphene

from .query import Query, Mutation, TYPES

SCHEMA = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=TYPES
)
