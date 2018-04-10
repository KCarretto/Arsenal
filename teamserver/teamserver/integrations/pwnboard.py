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
        PWNBOARD_URL: the domain that the pwnboard is living on with protocal
        (e.g. https://pwnboard.local/generic)
    """

    def __init__(self, config):
        """
        Initialize the integration.
        """
        self.url = config.get("PWNBOARD_URL", "https://pwnboard.local/generic")
    
    def __str__(self):
        """
        Return the integration name as the string.
        """
        return 'pwnboard-integration'

    def run(self, event_data, **kwargs):
        """
        Post an update to the pwnboard
        """
        
        headers = {'Content-Type': 'application/json',
                   'Connection': 'Close'}
        data = json.dumps({'ip': "10.3.3.2", 'type': "arsenal"})
        try:
            req = requests.post(host, data=data, headers=headers, timeout=3)
            print(req.text)
            return True
        except Exception as E:
            return False
