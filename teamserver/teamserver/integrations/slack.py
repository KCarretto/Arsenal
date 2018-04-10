"""
    This module integrates the teamserver with slack, and notifies
    a slack channel about events.
"""
import time
from datetime import datetime

from slackclient import SlackClient

from .integration import Integration


class SlackIntegration(Integration):
    """
    Handle integration with slack.

    Configuration:
        API_TOKEN: The slack API token.
        TIMEOUT: The maximum amount of time to wait for a message post.

        ERROR_CHANNEL: The channel that error messages are posted to.
        ACTION_CHANNEL: The channel that action messages are posted to.
    """
    client = None
    timeout = 10

    def __init__(self, config):
        """
        Initialize the integration.
        """
        self.config = config
        self.timeout = config.get('TIMEOUT', 10)
        self.client = SlackClient(config.get('API_TOKEN'))

    def __str__(self):
        """
        Return the integration name as the string.
        """
        return 'slack-integration'

    def post_message(self, channel, message):
        """
        Post a message to slack.
        """
        self.client.api_call(
            'chat.postMessage',
            channel=channel,
            text=message,
            timeout=self.timeout,
            as_user=True,
        )

    def handle_error(self, event_data):
        """
        Handle an 'logged_error' event.
        """
        entry = event_data.get('log')
        timestamp = datetime.fromtimestamp(
            entry.get('timestamp', time.time())).strftime('%Y-%m-%d %H:%M:%S')

        self.post_message(
            self.config.get('ERROR_CHANNEL'),
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
        message = 'Action Completed: [{}] {} {}'.format(
            action.status,
            action.target_name,
            action.action_string,
        )
        self.post_message(
            self.config.get('ACTION_CHANNEL'),
            message,
        )

    def run(self, event_data, **kwargs):
        """
        Notify slack of an event.
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
