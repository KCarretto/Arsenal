"""
    This module tests basic functionality of the group action API.
"""
import sys
import unittest

try:
    from testutils import BaseTest, Database, APIClient
    from teamserver.config import ACTION_STATUSES, GROUP_ACTION_STATUSES
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils import BaseTest, Database, APIClient
    from teamserver.config import ACTION_STATUSES, GROUP_ACTION_STATUSES

class GroupActionAPITest(BaseTest):
    """
    This class is used to test the Group Action API functions.
    """
    def test_create(self):
        """
        This test will pass if the group action is created and content matches.
        """
        targets = [
            Database.create_target().name,
            Database.create_target().name,
            Database.create_target().name,
            Database.create_target().name,
        ]
        group = Database.create_group('TEST', targets)
        data = APIClient.create_group_action(self.client, group.name, 'exec echo hello | wall')
        self.assertEqual(data['error'], False)
        group_action = Database.get_group_action(data['group_action_id'])
        self.assertIsNotNone(group_action)
        self.assertEqual(group_action.action_string, 'exec echo hello | wall')
        for action in group_action.actions:
            self.assertEqual(action.action_string, 'exec echo hello | wall')

    def test_get(self):
        """
        This test will pass if it finds the correct group action.
        """
        group_action = Database.create_group_action()
        data = APIClient.get_group_action(self.client, group_action.group_action_id)
        self.assertEqual(data['error'], False)
        self.assertListEqual(
            sorted(data['group_action']['action_ids']),
            sorted(group_action.action_ids)
        )

    def test_cancel(self):
        """
        This test will pass if an action is successfully cancelled.
        """
        group_action = Database.create_group_action()
        self.assertEqual(group_action.cancelled, False)
        data = APIClient.cancel_group_action(self.client, group_action.group_action_id)
        self.assertEqual(data['error'], False)
        group_action = Database.get_group_action(group_action.group_action_id)
        self.assertEqual(group_action.cancelled, True)
        self.assertEqual(
            group_action.get_status(),
            GROUP_ACTION_STATUSES.get('cancelled', 'cancelled'))
        for action in group_action.actions:
            self.assertEqual(action.cancelled, True)
            self.assertEqual(action.status, ACTION_STATUSES.get('cancelled', 'cancelled'))

    def test_list(self):
        """
        This test will create a few action objects through the API, and then test listing them.
        """
        group_actions = [
            Database.create_group_action().group_action_id,
            #Database.create_group_action().group_action_id,
            #Database.create_group_action().group_action_id,
            #Database.create_group_action().group_action_id,
            #Database.create_group_action().group_action_id,
        ]
        data = APIClient.list_group_actions(self.client)
        self.assertEqual(data['error'], False)
        self.assertListEqual(
            sorted(list(data['group_actions'].keys())),
            sorted(group_actions)
        )

if __name__ == '__main__':
    unittest.main()
