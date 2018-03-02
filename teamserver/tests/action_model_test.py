"""
    This module tests basic functionality of the target model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import os
import sys
import time
import unittest

from testutils import ModelTest, create_test_target, create_test_action, get_action #pylint: disable=no-name-in-module
from testutils import create_test_session, create_test_response, missing_session #pylint: disable=no-name-in-module
from testutils import parse_action_string #pylint: disable=no-name-in-module

# Configure path to include teamserver module
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from teamserver.config import ACTION_STATUSES, ACTION_STALE_THRESHOLD #pylint: disable=wrong-import-position
from teamserver.config import ACTION_TYPES, DEFAULT_SUBSET #pylint: disable=wrong-import-position
class ActionModelTest(ModelTest):
    """
    This class is used to test the teamserver's action model class.
    """

    TEST_ACTION_STRING = 'echo hello world'
    TEST_ACTION_TYPE = '0'

    def test_create_pass(self):
        """
        This test will attempt to create an action model object.
        """

        target = create_test_target()
        action = create_test_action(target.name, self.TEST_ACTION_STRING, self.TEST_ACTION_TYPE)
        self.assertEqual(action.target_name, target.name)
        self.assertEqual(action.action_string, self.TEST_ACTION_STRING)
        self.assertEqual(action.action_type, self.TEST_ACTION_TYPE)

    def test_find_pass(self):
        """
        This test will attempt to create an action model object,
        save it to the database, and then find it.
        """
        action1 = create_test_action()
        action2 = get_action(action1.action_id)
        self.assertEqual(action1, action2)

    def test_status_pass(self):
        """
        This test will attempt to see if the action is assigned
        the correct statuses based on it's session.
        """
        action1 = create_test_action()
        self.assertIsNone(action1.session_id)
        self.assertEqual(action1.status, ACTION_STATUSES.get('queued'))

        action1.queue_time = time.time() - (ACTION_STALE_THRESHOLD+1)
        action1.save()
        self.assertEqual(action1.status, ACTION_STATUSES.get('stale'))

        session1 = create_test_session()
        action1.assign_to(session1)
        self.assertEqual(action1.status, ACTION_STATUSES.get('sent'))

        missing_session(session1)
        self.assertEqual(action1.status, ACTION_STATUSES.get('failing'))

        session1.timestamp = 0
        session1.save()
        self.assertEqual(action1.status, ACTION_STATUSES.get('failed'))

        session1.timestamp = time.time()
        session1.save()
        response = create_test_response(None, None, True)
        action1.submit_response(response)
        self.assertEqual(action1.status, ACTION_STATUSES.get('error'))

        response.error = False
        action1.submit_response(response)
        self.assertEqual(action1.status, ACTION_STATUSES.get('complete'))

    def test_action_parse_basic_format(self):
        """
        This function tests the Action model's parser, ensuring that
        commands parse into the proper dictionaries.
        """
        test_time = time.time()+120

        final_config = {
            'interval': 300,
            'interval_delta': 20,
            'servers': ['10.80.100.10', 'https://bobzinga.com'],
        }

        action_tests = [
            # config
            (
                parse_action_string('config {} {} {}'.format(
                    '--interval 300',
                    '--delta 20',
                    '--servers 10.80.100.10 https://bobzinga.com')),
                {
                    'action_type': ACTION_TYPES.get('config', 0),
                    'config': final_config
                }
            ),
            # exec
            (
                parse_action_string('exec ls'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'ls',
                    'args': []
                }
            ),
            # exec with args
            (
                parse_action_string('exec ls -al'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'ls',
                    'args': ['-al']
                }
            ),
            # timed exec
            (
                parse_action_string('exec --time={} ls -al'.format(test_time)),
                {
                    'action_type': ACTION_TYPES.get('timed_exec', 2),
                    'command': 'ls',
                    'args': ['-al'],
                    'start_time': test_time
                }
            ),
            # spawn
            (
                parse_action_string('exec --spawn ls -al'),
                {
                    'action_type': ACTION_TYPES.get('spawn', 3),
                    'command': 'ls',
                    'args': ['-al'],
                }
            ),
            # timed spawn
            (
                parse_action_string('exec --time={} --spawn ls -al'.format(test_time)),
                {
                    'action_type': ACTION_TYPES.get('timed_spawn', 4),
                    'command': 'ls',
                    'args': ['-al'],
                    'start_time': test_time
                }
            ),
            # timed spawn (swapped args)
            (
                parse_action_string('exec --spawn --time={} ls -al'.format(test_time)),
                {
                    'action_type': ACTION_TYPES.get('timed_spawn', 4),
                    'command': 'ls',
                    'args': ['-al'],
                    'start_time': test_time
                }
            ),
            # upload
            (
                parse_action_string('upload files/sshd_config /etc/ssh/sshd_config'),
                {
                    'action_type': ACTION_TYPES.get('upload', 5),
                    'remote_path': '/etc/ssh/sshd_config',
                    'teamserver_path': 'files/sshd_config'
                }
            ),
            # download
            (
                parse_action_string('download /etc/passwd files/passwd'),
                {
                    'action_type': ACTION_TYPES.get('download', 6),
                    'remote_path': '/etc/passwd',
                    'teamserver_path': 'files/passwd'
                }
            ),
            # gather default
            (
                parse_action_string('gather'),
                {
                    'action_type': ACTION_TYPES.get('gather', 7),
                    'subset': DEFAULT_SUBSET
                }
            ),
            # gather min
            (
                parse_action_string('gather -s min'),
                {
                    'action_type': ACTION_TYPES.get('gather', 7),
                    'subset': 'min'
                }
            ),
        ]

        for test in action_tests:
            self.assertDictEqual(test[0], test[1])

    def test_exec_parsing(self):
        """
        Perform more extensive tests on exec.
        """
        action_tests = [
            # pipe
            (
                parse_action_string('exec echo hi | tee output.txt'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'echo',
                    'args': ['hi', '|', 'tee', 'output.txt']
                }
            ),
            # conflicting args
            (
                parse_action_string('exec date --time time'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'date',
                    'args': ['--time', 'time']
                }
            ),
        ]
        for test in action_tests:
            self.assertDictEqual(test[0], test[1])

if __name__ == '__main__':
    unittest.main()
