"""
This module is responsible for event handling and management.
"""
import requests

from celery import Celery
from mongoengine import connect

from teamserver.integrations import Integration, SlackIntegration
from teamserver.models import Webhook
from teamserver.config import CELERY_MAIN_NAME, CELERY_RESULT_BACKEND, CELERY_BROKER_URL
from teamserver.config import CELERY_BROKER_TRANSPORT
from teamserver.config import DB_NAME, DB_HOST, DB_PORT
from teamserver.config import CONNECT_TIMEOUT, READ_TIMEOUT, INTEGRATIONS


app = Celery( # pylint: disable=invalid-name
    CELERY_MAIN_NAME,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
    broker_transport_options=CELERY_BROKER_TRANSPORT,
)


connect(DB_NAME, host=DB_HOST, port=DB_PORT)

SLACK = SlackIntegration(INTEGRATIONS.get('SLACK_CONFIG', {'enabled': False}))

@app.task
def notify_subscriber(**kwargs):
    """
    Notify a subscriber with the given data.
    """
    print('Notifying subscriber: {}'.format(kwargs.get('post_url')))
    requests.post(
        kwargs.get('posturl'),
        json=kwargs.get('data'),
        timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
    )

@app.task
def notify_integration(integration, data):
    """
    Trigger an integration with the given data.
    """
    if integration and isinstance(integration, Integration):
        print('Notifying integration: {}'.format(str(integration)))
        integration.run(data)

@app.task
def trigger_event(**kwargs):
    """
    Trigger an event, and notify subscribers.
    """
    event = kwargs.get('event')
    print('Triggering event {}'.format(event))

    # Trigger Webhooks
    subscribers = Webhook.get_subscribers(event)
    if subscribers and event:
        for subscriber in subscribers:
            notify_subscriber.delay(
                post_url=subscriber.post_url,
                data=kwargs
            )
    elif event:

        # Notify Integrations
        notify_integration(SLACK, **kwargs)

