"""
    This module provides a base class for integrations to inherit from.
"""
from abc import ABCMeta, abstractmethod

class Integration(metaclass=ABCMeta): # pylint: disable=too-few-public-methods
    """
    Provide an abstract class for integrations to inherit from.
    """
    @abstractmethod
    def run(self, event_data, **kwargs):
        """
        Invoke the integration using event data and the integration's config.
        """
        pass
