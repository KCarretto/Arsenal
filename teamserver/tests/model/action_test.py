"""
    This module tests basic functionality of the target model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import sys
import time
import unittest

try:
    from testutils.test_cases import BaseTest
    from testutils.database import Database
    from teamserver.config import ACTION_STATUSES, ACTION_STALE_THRESHOLD
    from teamserver.config import ACTION_TYPES, DEFAULT_SUBSET
    from teamserver.models.action import Action
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils.test_cases import BaseTest
    from tests.testutils.database import Database
    from teamserver.config import ACTION_STATUSES, ACTION_STALE_THRESHOLD
    from teamserver.config import ACTION_TYPES, DEFAULT_SUBSET
    from teamserver.models.action import Action

class ActionModelTest(BaseTest):
    """
    This class is used to test the teamserver's action model class.
    """
    TEST_ACTION_STRING = 'exec echo hello world'

    def test_create_pass(self):
        """
        This test will attempt to create an action model object.
        """
        target = Database.create_target()
        action = Database.create_action(target.name, self.TEST_ACTION_STRING)
        self.assertEqual(action.target_name, target.name)
        self.assertEqual(action.action_string, self.TEST_ACTION_STRING)
        self.assertEqual(action.action_type, ACTION_TYPES.get('exec', 1))
        self.assertEqual(action.bound_session_id, '')
        self.assertIsNone(action.session_id)

    def test_find_pass(self):
        """
        This test will attempt to create an action model object,
        save it to the database, and then find it.
        """
        action1 = Database.create_action()
        action2 = Database.get_action(action1.action_id)
        self.assertIsNotNone(action1)
        self.assertIsNotNone(action2)
        self.assertEqual(action1, action2)
        self.assertEqual(action1.action_id, action2.action_id)

    def test_status_pass(self):
        """
        This test will attempt to see if the action is assigned
        the correct statuses based on it's session.
        """
        action1 = Database.create_action()
        self.assertIsNone(action1.session_id)
        self.assertEqual(action1.status, ACTION_STATUSES.get('queued'))

        action1.cancelled = True
        self.assertEqual(action1.status, ACTION_STATUSES.get('cancelled'))
        action1.cancelled = False

        action1.queue_time = time.time() - (ACTION_STALE_THRESHOLD+1)
        action1.save()
        self.assertEqual(action1.status, ACTION_STATUSES.get('stale'))

        session1 = Database.create_session()
        action1.assign_to(session1)
        self.assertEqual(action1.status, ACTION_STATUSES.get('sent'))

        Database.missing_session(session1)
        self.assertEqual(action1.status, ACTION_STATUSES.get('failing'))

        session1.timestamp = 0
        session1.save()
        self.assertEqual(action1.status, ACTION_STATUSES.get('failed'))

        session1.timestamp = time.time()
        session1.save()
        response = Database.create_response(None, None, True)
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
                Database.parse_action_string('config {} {} {}'.format(
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
                Database.parse_action_string('exec ls'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'ls',
                    'args': []
                }
            ),
            # exec with args
            (
                Database.parse_action_string('exec ls -al'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'ls',
                    'args': ['-al']
                }
            ),
            # timed exec
            (
                Database.parse_action_string('exec --time={} ls -al'.format(test_time)),
                {
                    'action_type': ACTION_TYPES.get('timed_exec', 2),
                    'command': 'ls',
                    'args': ['-al'],
                    'start_time': test_time
                }
            ),
            # spawn
            (
                Database.parse_action_string('exec --spawn ls -al'),
                {
                    'action_type': ACTION_TYPES.get('spawn', 3),
                    'command': 'ls',
                    'args': ['-al'],
                }
            ),
            # timed spawn
            (
                Database.parse_action_string('exec --time={} --spawn ls -al'.format(test_time)),
                {
                    'action_type': ACTION_TYPES.get('timed_spawn', 4),
                    'command': 'ls',
                    'args': ['-al'],
                    'start_time': test_time
                }
            ),
            # timed spawn (swapped args)
            (
                Database.parse_action_string('exec --spawn --time={} ls -al'.format(test_time)),
                {
                    'action_type': ACTION_TYPES.get('timed_spawn', 4),
                    'command': 'ls',
                    'args': ['-al'],
                    'start_time': test_time
                }
            ),
            # upload
            (
                Database.parse_action_string('upload files/sshd_config /etc/ssh/sshd_config'),
                {
                    'action_type': ACTION_TYPES.get('upload', 5),
                    'remote_path': '/etc/ssh/sshd_config',
                    'teamserver_path': 'files/sshd_config'
                }
            ),
            # download
            (
                Database.parse_action_string('download /etc/passwd files/passwd'),
                {
                    'action_type': ACTION_TYPES.get('download', 6),
                    'remote_path': '/etc/passwd',
                    'teamserver_path': 'files/passwd'
                }
            ),
            # gather default
            (
                Database.parse_action_string('gather'),
                {
                    'action_type': ACTION_TYPES.get('gather', 7),
                    'subset': DEFAULT_SUBSET
                }
            ),
            # gather min
            (
                Database.parse_action_string('gather -s min'),
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
                Database.parse_action_string('exec echo hi | tee output.txt'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'echo',
                    'args': ['hi', '|', 'tee', 'output.txt']
                }
            ),
            # conflicting args
            (
                Database.parse_action_string('exec date --time time'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'date',
                    'args': ['--time', 'time']
                }
            ),
            # subshell
            (
                Database.parse_action_string('exec find $(which bash)'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'find',
                    'args': ['$(which', 'bash)']
                }
            ),
            # backtick subshell
            (
                Database.parse_action_string('exec rm -rf `which bash`'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'rm',
                    'args': ['-rf', '`which', 'bash`']
                }
            ),
            # special chars (must be quoted)
            (
                Database.parse_action_string('exec echo -e "Hello \n World"'),
                {
                    'action_type': ACTION_TYPES.get('exec', 1),
                    'command': 'echo',
                    'args': ['-e', 'Hello \n World']
                }
            ),
        ]
        for test in action_tests:
            self.assertDictEqual(test[0], test[1])

    def test_get_unassigned_actions(self):
        """
        This test ensures that the proper unassigned actions are returned for a target.
        """
        target = Database.create_target()
        action1 = Database.create_action(target.name, 'exec echo hello')
        action2 = Database.create_action(target.name, 'exec echo world')

        actions = Action.get_target_unassigned_actions(target.name)

        for action in actions:
            self.assertIn(action.action_id, [action1.action_id, action2.action_id])
        self.assertEqual(len(actions), 2)


if __name__ == '__main__':
    unittest.main()
