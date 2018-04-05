"""
This module is responsible for event handling and management.
"""
import time
import requests

from celery import Celery

from teamserver.config import CELERY_MAIN_NAME, CELERY_RESULT_BACKEND, CELERY_BROKER_URL
from teamserver.models import Webhook

app = Celery( # pylint: disable=invalid-name
    CELERY_MAIN_NAME,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
)

@app.task
def trigger_event(**kwargs):
    """
    Trigger an event, and notify subscribers.
    """
    print("Triggering event")
    time.sleep(15)
    #event = kwargs.get('event')
    #subscribers = Webhook.get_subscribers(event)

    #if subscribers:
    #    kwargs['subscribers'] = [subscriber.document for subscriber in subscribers]

    requests.post('http://129.21.106.18', json=kwargs)

