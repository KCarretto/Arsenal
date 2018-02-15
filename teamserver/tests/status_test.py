"""
    This module tests basic functionality of the flask app,
    and ensures a proper status is returned from the /status endpoint.
"""
import sys
import os
import unittest

# Configure path to include teamserver module
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

import teamserver

def create_test_app():
    """
    This function creates the flask application with test values.
    """
    return teamserver.create_app(TESTING=True)

class StatusTest(unittest.TestCase):
    """
    This class is used to test the flask application's /status route.
    """
    def setUp(self):
        self.test_app = create_test_app()
        self.test_app.testing = True
        self.client = self.test_app.test_client()

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
        print(resp.data)
        self.assertIn('"error": false', str(resp.data))

if __name__ == '__main__':
    unittest.main()

