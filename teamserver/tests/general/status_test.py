"""
    This module tests basic functionality of the flask app,
    and ensures a proper status is returned from the /status endpoint.
"""

import sys
import unittest

try:
    from testutils.test_cases import BaseTest #pylint: disable=no-name-in-module
except ModuleNotFoundError:
    from os.path import abspath, dirname
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils.test_cases import BaseTest #pylint: disable=no-name-in-module

class StatusTest(BaseTest): # pylint: disable=too-few-public-methods
    """
    This class is used to test the flask application's /status route.
    """
    def test_status(self):
        """
        This test will pass if the /status endpoint returns no errors.
        """
        resp = self.client.get('/status')
        self.assertIn('"error": false', str(resp.data))

if __name__ == '__main__':
    unittest.main()

