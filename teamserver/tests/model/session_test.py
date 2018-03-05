"""
    This module tests basic functionality of the session model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import sys
import time
import unittest

try:
    from testutils.test_cases import ModelTest
    from testutils.database import Database
    from teamserver.config import SESSION_STATUSES, SESSION_CHECK_THRESHOLD, SESSION_CHECK_MODIFIER
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from teamserver.config import SESSION_STATUSES, SESSION_CHECK_THRESHOLD, SESSION_CHECK_MODIFIER
    from tests.testutils.test_cases import ModelTest
    from tests.testutils.database import Database

class SessionModelTest(ModelTest):
    """
    This class is used to test the teamserver's session model class.
    """
    def test_create_pass(self):
        """
        This test will attempt to create a session model object.
        """
        timestamp = time.time()
        session = Database.create_session('TEST', timestamp)
        self.assertEqual(session.target_name, 'TEST')
        self.assertEqual(session.timestamp, timestamp)
        self.assertIsNotNone(session.history)
        self.assertIsNotNone(session.servers)
        self.assertIsNotNone(session.interval)
        self.assertIsNotNone(session.interval_delta)

    def test_find_pass(self):
        """
        This test creates a session and attempts to find it,
        it's target, and it's history document.
        """
        session1 = Database.create_session()

        session2 = Database.get_session(session1.session_id)
        self.assertEqual(session1, session2)

        self.assertIsNotNone(Database.get_target(session2.target_name))

        self.assertIsNotNone(session1.history)
        self.assertIsNotNone(session2.history)

    def test_status_pass(self):
        """
        This tests to ensure the session's status is being set properly.
        """
        session1 = Database.create_session('TEST1', time.time())
        self.assertEqual(session1.status, SESSION_STATUSES.get('active'))

        missing_timer = 2401 + SESSION_CHECK_THRESHOLD

        session2 = Database.create_session('TEST2', time.time() - missing_timer, 1800, 600)
        self.assertEqual(session2.status, SESSION_STATUSES.get('missing'))

        missing_timer *= SESSION_CHECK_MODIFIER
        session3 = Database.create_session('TEST3', time.time() - missing_timer, 1800, 600)
        self.assertEqual(session3.status, SESSION_STATUSES.get('inactive'))

    def test_target_status_pass(self):
        """
        This tests to ensure a target's status is being set properly
        based on it's session statuses.
        """
        session1 = Database.create_session(None, 0)
        target = Database.get_target(session1.target_name)
        self.assertEqual(target.status, SESSION_STATUSES.get('inactive'))

        missing_timer = 2401 + SESSION_CHECK_THRESHOLD
        session2 = Database.create_session(target.name, time.time() - missing_timer, 1800, 600)
        self.assertEqual(target.status, SESSION_STATUSES.get('missing'))

        session3 = Database.create_session(target.name)
        self.assertEqual(target.status, SESSION_STATUSES.get('active'))

        session3.timestamp = 0
        session3.save()
        self.assertEqual(target.status, SESSION_STATUSES.get('missing'))

        session2.timestamp = 0
        session2.save()
        self.assertEqual(target.status, SESSION_STATUSES.get('inactive'))


if __name__ == '__main__':
    unittest.main()
