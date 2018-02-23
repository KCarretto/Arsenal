"""
    This module tests basic functionality of the session model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import os
import sys
import time
import unittest

from testutils import ModelTest, create_test_session #pylint: disable=no-name-in-module

# Configure path to include teamserver module
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from teamserver.config import SESSION_STATUSES, SESSION_CHECK_THRESHOLD, SESSION_CHECK_MODIFIER #pylint: disable=wrong-import-position

class SessionModelTest(ModelTest):
    """
    This class is used to test the teamserver's session model class.
    """
    def test_create_pass(self):
        """
        This test will attempt to create a session model object.
        """
        timestamp = time.time()
        session = create_test_session("TEST", timestamp)
        self.assertEqual(session.target_name, "TEST")
        self.assertEqual(session.timestamp, timestamp)
        self.assertIsNotNone(session.history)
        self.assertIsNotNone(session.servers)
        self.assertIsNotNone(session.interval)
        self.assertIsNotNone(session.interval_delta)

    def test_status_pass(self):
        """
        This tests to ensure the session's status is being set properly.
        """
        session1 = create_test_session("TEST1", time.time())
        self.assertEqual(session1.status, SESSION_STATUSES.get('active'))

        missing_timer = 2401 + SESSION_CHECK_THRESHOLD

        session2 = create_test_session("TEST2", time.time() - missing_timer, 1800, 600)
        self.assertEqual(session2.status, SESSION_STATUSES.get('missing'))

        missing_timer *= SESSION_CHECK_MODIFIER
        session3 = create_test_session("TEST3", time.time() - missing_timer, 1800, 600)
        self.assertEqual(session3.status, SESSION_STATUSES.get('inactive'))

if __name__ == '__main__':
    unittest.main()
