"""
    This module integrates the teamserver with slack, and notifies
    a slack channel about events.
"""
import time
import requests
from datetime import datetime

from .integration import Integration


class SlackIntegration(Integration):
    """
    Handle integration with workplace.

    Configuration:
        API_TOKEN: The workplace API token.
        TIMEOUT: The maximum amount of time to wait for a message post.

    """
    API_TOKEN = None
    timeout = 10
    workplace_api_url = ""

    def __init__(self, config):
        """
        Initialize the integration.
        """
        self.config = config
        self.timeout = config.get('TIMEOUT', 10)
        self.API_TOKEN = config.get('API_TOKEN')
        self.workplace_api_url = config.get('URL')

    def __str__(self):
        """
        Return the integration name as the string.
        """
        return 'workplace-integration'

    def post_message(self, thread_key, message):
        """
        Post a message to slack.
        """
        post_data = {
            "recipient": {"thread_key": thread_key},
            "message": {"text": message}
        }
        requests.post(
            "{}?access_token={}".format(self.workplace_api_url, self.API_TOKEN),
            json=post_data,
            timeout=self.timeout,
        )

    def handle_error(self, event_data):
        """
        Handle an 'logged_error' event.
        """
        entry = event_data.get('log')
        timestamp = datetime.fromtimestamp(
            entry.get('timestamp', time.time())).strftime('%Y-%m-%d %H:%M:%S')

        self.post_message(
            self.config.get('ERROR_THREAD'),
            'ERROR: [{}][{}]\t[{}] {}'.format(
                str(entry.get('level')),
                str(timestamp),
                str(entry.get('application')),
                str(entry.get('message')),
            )
        )

    def handle_action(self, event_data):
        """
        Handle an 'action_complete' event.
        """
        action = event_data.get('action')
        message = 'Action Completed (id: `{}`) [{}] {} `{}`'.format(
            action.get('action_id'),
            action.get('status'),
            action.get('target_name'),
            action.get('action_string'),
        )
        self.post_message(
            self.config.get('ACTION_THREAD'),
            message,
        )

    def run(self, event_data, **kwargs):
        """
        Notify workchat of an event.
        """
        if not self.config.get('enabled', False):
            return

        handled_events = {
            'logged_error': self.handle_error,
            'action_complete': self.handle_action,
        }
        method = handled_events.get(event_data.get('event', ''))
        if method and callable(method):
            method(event_data)
