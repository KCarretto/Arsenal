"""
This module is responsible for event handling and management.
"""
from celery import Celery
from ..config import CELERY_MAIN_NAME, CELERY_RESULT_BACKEND, CELERY_BROKER_URL

CELERY = Celery(
    CELERY_MAIN_NAME,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
)

@CELERY.task
def trigger_event(data):
    """
    Trigger an event, and notify subscribers.
    """
    print(data)
