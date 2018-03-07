"""
    This module tests basic functionality of the group API.
"""

import sys
import unittest

from mongoengine.errors import DoesNotExist

try:
    from testutils import BaseTest, Database, APIClient
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils import BaseTest, Database, APIClient

class GroupAPITest(BaseTest):
    """
    This class is used to test the Action API functions.
    """
    def test_create(self):
        """
        Test the CreateGroup API function.
        """
        data = APIClient.create_group(self.client, 'SOME GROUP')
        self.assertEqual(data['error'], False)
        self.assertIsNotNone(Database.get_group('SOME GROUP'))

    def test_get(self):
        """
        Test the GetGroup API function.
        """
        targets = [
            Database.create_target(),
            Database.create_target(),
            Database.create_target(),
        ]
        Database.create_group('TEST GROUP', [target.name for target in targets])

        data = APIClient.get_group(self.client, 'TEST GROUP')
        self.assertEqual(data['error'], False)

        self.assertEqual(data['group']['name'], 'TEST GROUP')
        self.assertListEqual(
            sorted(data['group']['whitelist_members']),
            sorted([target.name for target in targets]))

    def test_add_member(self):
        """
        Test the GetGroup API function.
        """
        Database.create_group('TEST GROUP')
        target = Database.create_target()

        data = APIClient.add_group_member(self.client, 'TEST GROUP', target.name)
        self.assertEqual(data['error'], False)

        group = Database.get_group('TEST GROUP')
        self.assertListEqual(group.whitelist_members, [target.name])

    def test_remove_member(self):
        """
        Test the RemoveGroupMember function.
        """
        targets = [
            Database.create_target().name,
            Database.create_target().name,
            Database.create_target().name,
        ]

        Database.create_group('REMOVE GROUP', targets)

        data = APIClient.remove_group_member(self.client, 'REMOVE GROUP', targets[0])
        self.assertEqual(data['error'], False)

        group = Database.get_group('REMOVE GROUP')

        self.assertListEqual(sorted(targets[1:]), sorted(group.member_names))

    def test_blacklist_member(self):
        """
        Test the BlacklistGroupMember function.
        """
        targets = [
            Database.create_target().name,
            Database.create_target().name,
            Database.create_target().name,
        ]

        Database.create_group('BLACKLIST GROUP', targets)

        data = APIClient.blacklist_group_member(self.client, 'BLACKLIST GROUP', targets[0])
        self.assertEqual(data['error'], False)

        group = Database.get_group('BLACKLIST GROUP')

        self.assertListEqual(sorted(targets[1:]), sorted(group.member_names))
        self.assertListEqual([targets[0]], group.blacklist_members)

    def test_delete(self):
        """
        Test the DeleteGroup function.
        """
        group = Database.create_group()
        data = APIClient.delete_group(self.client, group.name)
        self.assertEqual(data['error'], False)
        with self.assertRaises(DoesNotExist):
            Database.get_group(group.name)

    def test_list(self):
        """
        Populates the database with sample groups, and calls the list API
        function to ensure that all are returned.
        """
        groups = [
            Database.create_group(),
            Database.create_group(),
            Database.create_group(),
            Database.create_group(),
            Database.create_group(),
        ]
        data = APIClient.list_groups(self.client)
        self.assertEqual(data['error'], False)
        self.assertEqual(
            sorted(list(data['groups'].keys())),
            sorted([group.name for group in groups])
            )

if __name__ == '__main__':
    unittest.main()
