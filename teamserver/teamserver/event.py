"""
This module is responsible for event handling and management.
"""
#from flask import current_app
from celery import Task

CELERY = None

class ArsenalTask(Task):
    """
    Stuff
    """
    def run(self, *args, **kwargs):
        msg = kwargs.get('msg')
        print(msg)

    #def bind(self, app):
    #    print('Calling bind')
    #    print(CELERY)
    #    return super(ArsenalTask, self).bind(CELERY)


def generate_event(data):
    """
    Generates an event
    """
    worker = ArsenalTask()
    worker.apply_async(msg=data)
