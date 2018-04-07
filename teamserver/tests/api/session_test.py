"""
    This module tests basic functionality of the session API.
"""
import sys
import time
import unittest

try:
    from testutils.test_cases import BaseTest
    from testutils.database import Database
    from testutils.api import APIClient
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils.test_cases import BaseTest
    from tests.testutils.database import Database
    from tests.testutils.api import APIClient

class SessionAPITest(BaseTest):
    """
    This class is used to test the Session API functions.
    """
    def test_create(self):
        """
        This test will pass if the session is created.
        """
        target = Database.create_target()
        data = APIClient.create_session(self.client, target.mac_addrs)

        session_id = data['session_id']
        self.assertEqual(False, data['error'])
        session = Database.get_session(session_id)
        self.assertIsNotNone(session)

    def test_get(self):
        """
        This test will pass if it finds the correct session.
        """
        session_id = Database.create_session().session_id
        data = APIClient.get_session(self.client, session_id)
        self.assertEqual(False, data['error'])
        self.assertEqual(session_id, data['session']['session_id'])

    def test_check_in(self):
        """
        This test will ensure that the session check in function works properly.
        """
        target = Database.create_target()

        # Old action
        assigned_action_data = Database.create_action(target.name, 'exec echo hello')
        assigned_action = Database.get_action(assigned_action_data['action_id'])

        # New actions
        action1_data = Database.create_action(target.name, 'exec ls -al /usr/share')
        action1_id = action1_data['action_id']

        action2_data = Database.create_action(target.name, 'config -i 20')
        action2_id = action2_data['action_id']

        # Create Session
        session = Database.create_session(target.name)

        # Assign old action
        assigned_action.assign_to(session.session_id)

        # Session Check in, submit response for old action
        check_data = APIClient.session_check_in(
            self.client,
            session.session_id,
            [
                {
                    'action_id': assigned_action.action_id,
                    'stdout': 'hello',
                    'stderr': None,
                    'start_time': time.time()-15,
                    'end_time': time.time()-5,
                    'error': False,
                }])
        self.assertEqual(check_data['error'], False)
        self.assertEqual(check_data['session_id'], session.session_id)

        # Veryify old action has response
        assigned_action = Database.get_action(assigned_action.action_id)
        self.assertIsNotNone(assigned_action.response)
        self.assertEqual(assigned_action.response.stdout, 'hello')

        # Verify new actions
        actions_raw = [
            Database.get_action(action1_id),
            Database.get_action(action2_id)
        ]
        actions = {}
        for action in check_data['actions']:
            actions[action['action_id']] = action

        # Note that priorities are calculated when sessions retrieve actions, based on queue time
        # Therefore, they are not tracked in the database. We know what they should be though,
        # based on the order they were queued.
        agent_docs = [
            actions_raw[0].agent_document,
            actions_raw[1].agent_document
        ]
        agent_docs[0]['priority'] = 0
        agent_docs[1]['priority'] = 1

        self.assertDictEqual(actions[action1_id], agent_docs[0])
        self.assertDictEqual(actions[action2_id], agent_docs[1])

    def test_update_config(self):
        """
        This test will pass if the config is correctly set.
        """
        initial_config = {
            'some fact': 54,
            'some other fact': 'Pi',
            'A list fact': ['sdasd', 'asdasd']
        }

        session_id = Database.create_session(None, None, 25, 5, None, initial_config).session_id

        config_changes = {
            'new fact': 'So new, am I',
            'A list fact': ['asdasd', 'sdasd'],
            'some fact': 55
        }

        data = APIClient.update_session_config(
            self.client,
            session_id,
            50,
            10,
            ['10.10.10.10'],
            config_changes)

        final_config = {
            'interval': 50,
            'interval_delta': 10,
            'servers': ['10.10.10.10'],
            'new fact': 'So new, am I',
            'some other fact': 'Pi',
            'A list fact': ['asdasd', 'sdasd'],
            'some fact': 55
        }

        self.assertEqual(False, data['error'])
        self.assertDictEqual(final_config, data['config'])

    def test_list(self):
        """
        Populates the database with sample sessions, and calls the list API
        function to ensure that all are returned.
        """
        sessions = [
            Database.create_session(),
            Database.create_session(),
            Database.create_session(),
            Database.create_session(),
            Database.create_session(),
        ]
        data = APIClient.list_sessions(self.client)
        self.assertEqual(data['error'], False)
        self.assertEqual(
            sorted(list(data['sessions'].keys())),
            sorted([session.session_id for session in sessions])
            )

if __name__ == '__main__':
    unittest.main()
