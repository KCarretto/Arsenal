"""
    This module integrates the teamserver with the pwnboard notifying
    beacon callback
    https://github.com/micahjmartin/pwnboard
    Author: Micah Martin
"""
from .integration import Integration
import requests
import json

class PwnboardIntegration(Integration):
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
        # The headers for the callback
        headers = {'Content-Type': 'application/json',
                   'Connection': 'Close'}
        # Try to get teh agent string
        try:
            name = event_data.get("session", {}).get("agent_version")
        except Exception as E:
            name = "Arsenal"


        try:
            facts = event_data.get("facts", {})
            # Stolen from cli.getTarget
	    ip_addrs = []
            for iface in facts.get('interfaces', []):
                for addr in iface.get('ip_addrs', []):
                    ip_addrs.append(addr)
            if not ip_addrs:
                raise Exception("No IP Address to be passed to the pwnboard")
        except Exception as E:
            # If we dont have an IP, then we have nothing to update
            return False

        data = json.dumps({'ips': ip_addrs, 'type': name})
        try:
            req = requests.post(host, data=data, headers=headers, timeout=3)
            print(req.text)
            return True
        except Exception as E:
            return False
