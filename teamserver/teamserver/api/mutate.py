"""
Sdasdad
"""

import graphene

from .target import Target, CreateTarget

def get_create(object_model, arguments):
    class CreateMutation(graphene.Mutation):
        Arguments = arguments

        model = graphene.Field(object_model)

        def mutate(self, _, **kwargs):
            model = object_model._meta.model(**kwargs)
            model.save(force_insert=True)
            return CreateMutation(model=model)

    return CreateMutation

class TargetArguments:
    name = graphene.String(required=True)
    uuid = graphene.String(required=True)

    #target_name = graphene.String(required=True)
    #agent_version = graphene.String(required=True)
    #config = SessionConfigInput(required=True)

class Mutation(graphene.ObjectType):
    """
    Represents all possible data mutations.
    """

    create_target = get_create(Target, TargetArguments).Field()
    #create_target = CreateTarget.Field()
    #create_session = CreateSession.Field()


