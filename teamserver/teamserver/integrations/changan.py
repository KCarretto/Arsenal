"""
    This module integrates the teamserver with changan
    https://github.com/koalatea/changan
    Author: Ryan Whittier
"""
from .integration import Integration

class ChanganIntegration(Integration): #pylint: disable=too-few-public-methods
    """
    Configuration:
        URL: the domain for changan
    """
    def __init__(self, config):
        """
        Initialize that integration.
        """
        self.config = config
        self.url = config.get("URL", "https://changan.local:8080/generic")

    def __str__(self):
        """
        Return the integration name as a string.
        """
        return 'changan-integration'

    def handle_create_target(self, event_data):
        """
        nothing right now
        """
        pass

    def handle_target_name_change(self, event_data):
        """
        nothing right now
        """
        pass

    def run(self, event_data, **kwargs):
        """
        Post an update to changan
        """
        event = event_data.get("event")

        handled_events = {
            'one_event': self.handle_create_target,
            'two_event': self.handle_target_name_change,
        }
