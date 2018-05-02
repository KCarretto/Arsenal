"""
This module contains the schema for Target objects.
"""
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType

from teamserver import models

def get_type(mongo_model):
    """
    Create a new MongoengineObjectType for the given mongoengine model.
    """
    return type(
        '{}'.format(mongo_model.__name__),
        (MongoengineObjectType,),
        {
            'Meta': type(
                'Meta',
                (object,),
                {
                    'model': mongo_model,
                    'interfaces': (Node,)
                }
            )
        }
    )

Target = get_type(models.Target)
Session = get_type(models.Session)
SessionConfig = get_type(models.SessionConfig)
