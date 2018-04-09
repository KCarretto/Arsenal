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
from teamserver.utils import log
from teamserver.integrations import Integration, SlackIntegration


app = Celery( # pylint: disable=invalid-name
    CELERY_MAIN_NAME,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
)

connect(DB_NAME, host=DB_HOST, port=DB_PORT)

SLACK = SlackIntegration(INTEGRATIONS.get('SLACK_CONFIG', {'enabled': False}))

@app.task
def notify_subscriber(**kwargs):
    """
    Notify a subscriber with the given data.
    """
    requests.post(
        kwargs.get('posturl'),
        json=kwargs.get('data'),
        timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
    )

@app.task
def notify_integration(**kwargs):
    """
    Trigger an integration with the given data.
    """
    integration = kwargs.get('integration')
    if integration and isinstance(integration, Integration):
        integration.run(
            event_data=kwargs.get('event_data'),
            **kwargs
        )

@app.task
def trigger_event(**kwargs):
    """
    Trigger an event, and notify subscribers.
    """
    event = kwargs.get('event')

    # Trigger Webhooks
    subscribers = Webhook.get_subscribers(event)
    if subscribers and event:
        log('INFO', 'Triggering event ({}).'.format(event))
        for subscriber in subscribers:
            notify_subscriber.delay(
                post_url=subscriber.post_url,
                data=kwargs
            )
    elif event:
        log('INFO', 'Triggered event ({}) had no subscribers.'.format(event))

        # Notify Integrations
        notify_integration(integration=SLACK, event_data=kwargs)

