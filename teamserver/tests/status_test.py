"""
    This module tests basic functionality of the flask app,
    and ensures a proper status is returned from the /status endpoint.
"""
import unittest

from testutils import ModelTest #pylint: disable=no-name-in-module

class StatusTest(ModelTest):
    """
    This class is used to test the flask application's /status route.
    """
    def test_pass(self):
        """
        This test should always pass.
        """
        pass

    def test_status(self):
        """
        This test will pass if the /status endpoint returns no errors.
        """
        resp = self.client.get('/status')
        self.assertIn('"error": false', str(resp.data))

if __name__ == '__main__':
    unittest.main()

