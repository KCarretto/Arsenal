"""
This module is responsible for event handling and management.
"""
import requests

from celery import Celery
from mongoengine import connect

from teamserver.config import CELERY_MAIN_NAME, CELERY_RESULT_BACKEND, CELERY_BROKER_URL
from teamserver.config import DB_NAME, DB_HOST, DB_PORT
from teamserver.config import CONNECT_TIMEOUT, READ_TIMEOUT, INTEGRATIONS
from teamserver.models import Webhook

from teamserver.integrations import SlackIntegration

app = Celery( # pylint: disable=invalid-name
    CELERY_MAIN_NAME,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
)

connect(DB_NAME, host=DB_HOST, port=DB_PORT)

SLACK = SlackIntegration(INTEGRATIONS.get('SLACK_CONFIG', {'enabled': False}))

@app.task
def trigger_event(**kwargs):
    """
    Trigger an event, and notify subscribers.
    """
    event = kwargs.get('event')

    # Trigger Webhooks
    subscribers = Webhook.get_subscribers(event)
    if subscribers and event:
       #utils.log('INFO', 'Triggering event ({}).'.format(event))
        for subscriber in subscribers:
            requests.post(subscriber.post_url, json=kwargs, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
    elif event:
        pass
        #utils.log('INFO', 'Triggered event ({}) had no subscribers.'.format(event))

    # Notify Integrations
    SLACK.run(kwargs)
