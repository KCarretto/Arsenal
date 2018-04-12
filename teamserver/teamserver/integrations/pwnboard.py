"""
    This module integrates the teamserver with the pwnboard notifying
    beacon callback
    https://github.com/micahjmartin/pwnboard
    Author: Micah Martin
"""
import requests
from requests.exceptions import RequestException
from .integration import Integration


class PwnboardIntegration(Integration): # pylint: disable=too-few-public-methods
    """
    Configuration:
        URL: the domain that the pwnboard is living on with protocal
        (e.g. https://pwnboard.local/generic)
    """

    def __init__(self, config):
        """
        Initialize the integration.
        """
        self.config = config
        self.url = config.get("URL", "https://pwnboard.local/generic")

    def __str__(self):
        """
        Return the integration name as the string.
        """
        return 'pwnboard-integration'

    def run(self, event_data, **kwargs):
        """
        Post an update to the pwnboard
        """
        event = event_data.get("event")
        if event != "session_checkin":
            return False
        # The headers for the callback
        # headers = {'Content-Type': 'application/json',
        #            'Connection': 'Close'}
        # Try to get the agent string
        name = event_data.get("session", {}).get("agent_version", "Arsenal")
        # Get the facts
        facts = event_data.get("facts", {})
        # Stolen from cli.getTarget
        ip_addrs = []
        for iface in facts.get('interfaces', []):
            for addr in iface.get('ip_addrs', []):
                ip_addrs.append(addr)
        if not ip_addrs:
            # If we dont have an IP, then we have nothing to update
            return False

        data = {'ips': ip_addrs, 'type': name}
        try:
            req = requests.post(self.url, json=data, timeout=3)
            print(req.text)
            return True
        except RequestException:
            return False
