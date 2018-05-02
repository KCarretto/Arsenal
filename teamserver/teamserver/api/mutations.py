"""
This module contains standard CRUD mutations for mongoengine models.
"""

import graphene

def get_create(object_model, arguments):

    class CreateMutation(graphene.Mutation):
        Arguments = arguments

        model = graphene.Field(object_model)

        def mutate(self, _, **kwargs):
            model = object_model._meta.model(**kwargs)
            model.save(force_insert=True)
            return CreateMutation(model=model)

    return type(
        "create{}".format(object_model.__name__),
        (CreateMutation,),
        {
            "Arguments": arguments,
            "model": graphene.Field(object_model)
        }
    )

#    return CreateMutation

def get_update(object_model, arguments, custom_get=None):
    class UpdateMutation(graphene.Mutation):
        Arguments = arguments

        model = graphene.Field(object_model)

        def mutate(self, _, **kwargs):
            if custom_get and callable(custom_get):
                model = custom_get(**kwargs)
            else:
                model = object_model._meta.model.objects.get(**kwargs)

            model.update(**kwargs)
            model.reload()

            return UpdateMutation(model=model)

    return UpdateMutation

def get_delete(object_model, arguments, custom_get=None):
    class DeleteMutation(graphene.Mutation):
        Arguments = arguments

        ok = graphene.Boolean()

        def mutate(self, _, **kwargs):
            if custom_get and callable(custom_get):
                model = custom_get(**kwargs)
            else:
                model = object_model._meta.model.objects.get(**kwargs)

            model.delete()
            return DeleteMutation(ok=True)

    return DeleteMutation

