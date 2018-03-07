"""
    This module tests basic functionality of the action API.
"""
import sys
import unittest

try:
    from testutils import BaseTest, Database, APIClient
    from teamserver.config import ACTION_STATUSES, ACTION_TYPES
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils import BaseTest, Database, APIClient
    from teamserver.config import ACTION_STATUSES, ACTION_TYPES

class ActionAPITest(BaseTest):
    """
    This class is used to test the Action API functions.
    """
    def test_create(self):
        """
        This test will pass if the action is created and content matches.
        """
        target = Database.create_target()
        data = APIClient.create_action(self.client, target.name, 'exec ls -al /dir')
        action_id = data['action_id']
        self.assertEqual(False, data['error'])
        action = Database.get_action(action_id)
        self.assertIsNotNone(action)
        self.assertEqual(action.action_type, ACTION_TYPES.get('exec', 1))
        self.assertEqual(action.command, 'ls')
        self.assertListEqual(action.args, ['-al', '/dir'])
        self.assertEqual(action.cancelled, False)

    def test_get(self):
        """
        This test will pass if it finds the correct action.
        Note that this must use the CreateTarget API call because the
        action string needs to be parsed.
        """
        target = Database.create_target()
        action_id = Database.create_action(target.name, 'exec ls')['action_id']
        data = APIClient.get_action(self.client, action_id)
        action = Database.get_action(action_id)
        self.assertEqual(data['error'], False)
        self.assertIsNotNone(data['action'])
        self.assertEqual(action_id, action.action_id)
        self.assertEqual(target.name, action.target_name)
        self.assertEqual('ls', action.command)

    def test_cancel(self):
        """
        This test will pass if an action is successfully cancelled.
        """
        target = Database.create_target()
        action_id = Database.create_action(
            target.name,
            'exec echo hello world')['action_id']
        action = Database.get_action(action_id)
        self.assertEqual(action.cancelled, False)
        data = APIClient.cancel_action(self.client, action_id)
        self.assertEqual(data['error'], False)
        action = Database.get_action(action_id)
        self.assertEqual(action.status, ACTION_STATUSES.get('cancelled'))
        self.assertEqual(action.cancelled, True)

    def test_list(self):
        """
        This test will create a few action objects through the API, and then test listing them.
        """
        target = Database.create_target()
        test_actions = [
            Database.create_action(target.name, 'exec ls -al'),
            Database.create_action(target.name, 'config -i 20'),
            Database.create_action(target.name, 'exec --time 1345.12345 rm -rf tmp/'),
            Database.create_action(target.name, 'exec --spawn /bin/beloved'),
            Database.create_action(target.name, 'upload /some/file /another/file'),
            Database.create_action(target.name, 'download /lol/what /ha/nope'),
            Database.create_action(target.name, 'gather -s min')
        ]
        data = APIClient.list_actions(self.client)
        self.assertEqual(data['error'], False)

        for action in test_actions:
            self.assertIn(action['action_id'], data['actions'].keys())


if __name__ == '__main__':
    unittest.main()
