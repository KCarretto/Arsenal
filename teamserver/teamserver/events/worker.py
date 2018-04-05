"""
This module is responsible for event handling and management.
"""
import requests

from celery import Celery
from ..config import CELERY_MAIN_NAME, CELERY_RESULT_BACKEND, CELERY_BROKER_URL
from ..models import Webhook

CELERY = Celery(
    CELERY_MAIN_NAME,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
)

@CELERY.task
def trigger_event(**kwargs):
    """
    Trigger an event, and notify subscribers.
    """
    event = kwargs.get('event')
    subscribers = Webhook.get_subscribers(event)

    if subscribers:
        kwargs['subscribers'] = [subscriber.document for subscriber in subscribers]

    requests.post('http://129.21.106.18', json=kwargs)

