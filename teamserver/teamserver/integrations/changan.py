"""
    This module integrates the teamserver with changan
    https://github.com/koalatea/changan
    Author: Ryan Whittier
"""
import requests
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
        self.url = config.get("URL", "https://changan.koalatea.me:8080/")

    def __str__(self):
        """
        Return the integration name as a string.
        """
        return 'changan-integration'

    def handle_create_target(self, event_data):
        """
        nothing right now
        """
        try:
            interfaces = []
            for interface in event_data.get('target', {})['facts']['interfaces']:
                my_interface = {}
                my_interface['name'] = interface['name']
                my_interface['mac'] = interface['mac_addr']
                my_interface['ips'] = []
                for ip_addr in interface['ip_addrs']:
                    my_interface['ips'].append(ip_addr.split('/')[0])
                interfaces.append(my_interface)
            add_client_data = {'device_name': event_data['name'], 'interface': my_interface}
            requests.put('{}api/v1/devices'.format(self.url), json=add_client_data, verify=False)
        except Exception as exception: #pylint: disable=broad-except
            print(exception)

    def handle_target_name_change(self, event_data):
        """
        nothing right now
        """
        try:
            query_data = {'device_name': event_data['old_name']}
            resp = requests.get('{}api/v1/devices'.format(self.url), json=query_data, verify=False)
            device_id = resp.json().get('device_id', '')
            if device_id:
                change_data = {'device_id': device_id, 'device_name': event_data['new_name']}
                resp = requests.post('{}api/v1/devices'.format(self.url), json=change_data,
                                     verify=False)
        except Exception as exception: #pylint: disable=broad-except
            print(exception)

    def run(self, event_data, **kwargs):
        """
        Post an update to changan
        if not self.config.get('enabled', False):
        """

        handled_events = {
            'target_create': self.handle_create_target,
            'target_rename': self.handle_target_name_change,
        }
        method = handled_events.get(event_data.get('event', ''))
        if method and callable(method):
            method(event_data)
