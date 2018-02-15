import sys
import os
import unittest

# Configure path to include teamserver module
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

import teamserver

def create_test_app():
    return teamserver.create_app(TESTING=True)

class StatusTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_app = create_test_app()
        self.test_app.testing = True
        self.client = self.test_app.test_client()

    def test_pass(self):
        pass

    def test_status(self):
        resp = self.client.get('/status')
        print(resp.data)
        self.assertIn('"error": false', str(resp.data))

if __name__ == '__main__':
    unittest.main()

