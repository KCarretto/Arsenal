"""
    This module provides general utillities accessed by test cases.
"""
from uuid import uuid4

import os
import sys
import time
import unittest

# Configure path to include teamserver module
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from teamserver import create_app #pylint: disable=wrong-import-position
from teamserver.models.action  import Action, Response #pylint: disable=wrong-import-position
from teamserver.models.session import Session, SessionHistory #pylint: disable=wrong-import-position
from teamserver.models.target  import Target #pylint: disable=wrong-import-position

from teamserver.config import SESSION_CHECK_THRESHOLD #pylint: disable=wrong-import-position



class ModelTest(unittest.TestCase):
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
        clear_database()

    def test_pass(self):
        """
        This test should always pass.
        """
        pass

def clear_database():
    """
    This function drops all relevant collections in the database.
    """
    Target.drop_collection()
    Session.drop_collection()
    SessionHistory.drop_collection()

def create_test_app():
    """
    This function creates the flask application with test values.
    """
    return create_app(
        TESTING=True,
        MONGODB_SETTINGS=
        {
            'db': 'arsenal_test',
            'host': 'mongomock://localhost',
            'is_mock': True
        })

def get_session(session_id):
    """
    Queries for a session by id and returns it.
    """
    return Session.get_by_id(session_id)

def get_target(name):
    """
    Queries for a target by name and returns it.
    """
    return Target.get_by_name(name) #pylint: disable=no-member

def get_action(action_id):
    """
    Queries for an action by id and returns it.
    """
    return Action.get_by_id(action_id)

def parse_action_string(action_string):
    """
    Parses an action string.
    """
    return Action.parse_action_string(action_string)

def create_test_action(
        target_name=None,
        action_string=None,
        action_type=None,
        response=None,
        bound_session_id=None):
    """
    Creates a test action object and commits it to the database based
    on the given properties. If the properties are left empty, they will
    automatically be determined.
    """
    if target_name is None:
        target = create_test_target()
        target_name = target.name

    action_id = str(uuid4())

    action = Action(
        action_id=action_id,
        action_string=action_string if action_string is not None else 'echo test',
        action_type=action_type if action_type is not None else 0,
        target_name=target_name,
        bound_session_id=bound_session_id,
        queue_time=time.time(),
        response=response
    )
    action.save(force_insert=True)
    return action

def create_test_response(
        stdout=None,
        stderr=None,
        error=False,
        start_time=None,
        end_time=None
    ):
    """
    Creates a test response object for an action. You must assign this
    to an action and commit the changes to the database.
    """
    response = Response(
        stdout=stdout if stdout is not None else 'test',
        stderr=stderr if stderr is not None else '',
        error=error,
        start_time=start_time if start_time is not None else (time.time()-5),
        end_time=end_time if end_time is not None else time.time()
    )
    return response

def create_test_session(
        target_name=None,
        timestamp=None,
        interval=20,
        interval_delta=5,
        servers=None):
    """
    Creates a test session object and commits it to the database based
    on the given properties. This also creates a test SessionHistory.
    If the properties are left empty, they will automatically be determined.
    """
    if target_name is None:
        target = create_test_target()
        target_name = target.name

    session_id = str(uuid4())
    timestamp = timestamp if timestamp is not None else time.time()

    session_history = SessionHistory(
        session_id=session_id,
        checkin_timestamps=[timestamp]
    )
    session_history.save(force_insert=True)
    session = Session(
        session_id=session_id,
        target_name=target_name,
        servers=servers if servers is not None else ['8.8.8.8'],
        interval=interval,
        interval_delta=interval_delta,
        timestamp=timestamp
    )
    session.save(force_insert=True)
    return session

def missing_session(session):
    """
    This function updates a session's timestamp to force it's status
    to become missing.
    """
    missing_timer = session.interval + session.interval_delta + SESSION_CHECK_THRESHOLD + 1
    session.timestamp = time.time() - missing_timer
    session.save()

def create_test_target(
        name=None,
        facts=None,
        credentials=None,
        mac_addrs=None):

    """
    Creates a test target object and commits it to the database based
    on the given properties. If the properties are left empty, they will
    automatically be determined.
    """
    target = Target(
        name=name if name is not None else str(uuid4()),
        facts=facts if facts is not None else {
            'hostname': uuid4(),
            'interfaces': [
                {
                    'name': 'lo',
                    'mac_addr': str(uuid4),
                    'ip_addrs': ['127.0.0.1', '::1']
                },
                {
                    'name': 'eth0',
                    'mac_addr': str(uuid4),
                    'ip_addrs': ['192.168.0.1']
                }
            ]
        },
        mac_addrs=mac_addrs if mac_addrs is not None else [
            'AA:BB:CC:DD:EE:FF',
            str(uuid4())[0:17]
            ],
        credentials=credentials
    )
    target.save(force_insert=True)
    return target
