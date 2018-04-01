"""
    This module contains any Test Case objects that inherit from unittest.TestCase.
    Additionally, it will contain methods necessary for setup and teardown of those
    test cases.
"""
import sys
import unittest

try:
    from teamserver import create_app
    from teamserver.models import Action, GroupAction, Group, Session, SessionHistory, Target, Log
    from teamserver.config import APPLICATION
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import abspath, dirname
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from teamserver import create_app
    from teamserver.models import Action, GroupAction, Group, Session, SessionHistory, Target
    from teamserver.config import APPLICATION

def clear_database():
    """
    This function drops all relevant collections in the database.
    """
    Action.drop_collection()
    GroupAction.drop_collection()
    Group.drop_collection()
    Session.drop_collection()
    SessionHistory.drop_collection()
    Target.drop_collection()
    Log.drop_collection()

def create_test_app():
    """
    This function creates the flask application with test values.
    """
    return create_app(
        TESTING=True,
        DISABLE_AUTH=True,
        MONGODB_SETTINGS=
        {
            'db': 'arsenal_testing',
            'host': 'mongomock://localhost',
            'is_mock': True
        })

class BaseTest(unittest.TestCase):
    """
    This class is meant for unit tests to inherit from.
    It takes care of basics like setup and teardown, as well as a pass test.
    """
    def setUp(self):
        """
        This performs test setup operations.
        """
        self.test_app = create_test_app()
        self.test_app.testing = True
        self.client = self.test_app.test_client()
        clear_database()

    def tearDown(self):
        """
        This clears the database after each test.
        """
        for entry in Log.list_logs(False, APPLICATION):
            print('[{}]\t{}\t{}:\t{}'.format(
                entry.timestamp,
                entry.level,
                entry.application,
                entry.message))
        clear_database()

    def test_pass(self):
        """
        This test should always pass.
        """
        pass
