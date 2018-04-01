"""
    This module tests basic functionality of the group action model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import sys
import unittest

try:
    from testutils import BaseTest, Database
    from teamserver.models import GroupAction
    from teamserver.config import GROUP_ACTION_STATUSES, ACTION_STATUSES
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils import BaseTest, Database
    from teamserver.config import GROUP_ACTION_STATUSES, ACTION_STATUSES
    from teamserver.models import GroupAction

class GroupActionModelTest(BaseTest):
    """
    This class is used to test the teamserver's group action model class.
    """
    def test_create(self):
        """
        Attempt to create a GroupAction document
        """
        targets = [
            Database.create_target().name,
            Database.create_target().name,
            Database.create_target().name,
            Database.create_target().name,
            Database.create_target().name,
        ]
        Database.create_group('test_group', targets)
        group_action = Database.create_group_action('test_group', 'exec echo hi')
        self.assertEqual(group_action.cancelled, False)
        self.assertEqual(group_action.action_string, 'exec echo hi')
        for action in group_action.actions:
            self.assertEqual(action.action_string, 'exec echo hi')
            self.assertIn(action.target_name, targets)

    def test_get(self):
        """
        Attempt to fetch a GroupAction document
        """
        group_action1 = Database.create_group_action()
        group_action2 = Database.get_group_action(group_action1.group_action_id)
        self.assertEqual(group_action1.group_action_id, group_action2.group_action_id)

    def test_get_by_id(self):
        """
        Attempt to get a GroupAction by ID
        """
        group_action1 = Database.create_group_action().group_action_id
        group_action2 = GroupAction.get_by_id(group_action1)
        self.assertIsNotNone(group_action2)
        self.assertEqual(group_action1, group_action2.group_action_id)

    def test_status(self):
        """
        Ensure that the proper status is set for a group action
        based on it's included actions.
        """
        # After creation, status should be queued
        group_action = Database.create_group_action()
        self.assertEqual(group_action.get_status(), GROUP_ACTION_STATUSES.get('queued', 'queued'))

        # Send to a session, status should be in progress
        session = Database.create_session()
        group_action.actions[0].assign_to(session.session_id)
        self.assertEqual(
            group_action.get_status(),
            GROUP_ACTION_STATUSES.get('in progress', 'in progress'))

        # Submit a response to all actions, status should be success
        for action in group_action.actions:
            action.assign_to(session.session_id)
            response = Database.create_response()
            action.submit_response(response)
        self.assertEqual(group_action.get_status(), GROUP_ACTION_STATUSES.get('success', 'success'))

        # Create a new group action, make all actions stale. Status should be failed
        group_action = Database.create_group_action()
        for action in group_action.actions:
            action.queue_time = 0
            action.save()
        self.assertEqual(group_action.get_status(), GROUP_ACTION_STATUSES.get('failed', 'failed'))

        # Have a session check in, status should update to in progress
        group_action.actions[0].assign_to(session.session_id)
        self.assertEqual(
            group_action.get_status(),
            GROUP_ACTION_STATUSES.get('in progress', 'in progress'))

        # Submit a response, status should be mixed success
        response = Database.create_response()
        group_action.actions[0].submit_response(response)
        self.assertEqual(
            group_action.get_status(),
            GROUP_ACTION_STATUSES.get('mixed success', 'mixed success'))

        # Create a new group action, and cancel it. Status should be cancelled
        group_action = Database.create_group_action()
        group_action.cancel()
        self.assertEqual(
            group_action.get_status(),
            GROUP_ACTION_STATUSES.get('cancelled', 'cancelled'))

    def test_cancel(self):
        """
        Test cancelling a group action.
        """
        group_action = Database.create_group_action()
        group_action.cancel()
        for action in group_action.actions:
            self.assertEqual(action.status, ACTION_STATUSES.get('cancelled', 'cancelled'))
            self.assertEqual(action.cancelled, True)
        self.assertEqual(group_action.cancelled, True)

if __name__ == '__main__':
    unittest.main()
