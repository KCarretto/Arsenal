"""
    This module tests basic functionality of the group model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import sys
import unittest

from mongoengine import DoesNotExist

# pylint: disable=duplicate-code
try:
    from testutils import BaseTest, Database
    from teamserver.models import Group
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils import BaseTest, Database
    from teamserver.models import Group

class GroupModelTest(BaseTest):
    """
    This class is used to test the teamserver's group model class.
    """
    def test_target_groups(self):
        """
        Test the get_target_groups function.
        """
        target = Database.create_target()
        group1 = Database.create_group('group1')
        group2 = Database.create_group('group2')
        Database.create_group('group3')

        group1.whitelist_member(target)
        group2.whitelist_member(target)
        group_names = [group.name for group in Group.get_target_groups(target.name)]

        self.assertIn('group1', group_names)
        self.assertIn('group2', group_names)
        self.assertNotIn('group3', group_names)

    def test_get_by_name(self):
        """
        Test the get_by_name function.
        """
        Database.create_group('some group')
        Database.create_group('other group')
        group = Group.get_by_name('some group')
        self.assertEqual(group.name, 'some group')

        with self.assertRaises(DoesNotExist):
            Group.get_by_name('not group')

    def test_members(self):
        """
        Test the members function.
        """
        target1 = Database.create_target()
        target2 = Database.create_target()
        target3 = Database.create_target()
        group = Database.create_group('test_group')
        group.whitelist_member(target1)
        group.whitelist_member(target2)

        member_names = [member.name for member in group.members]

        self.assertIn(target1.name, member_names)
        self.assertIn(target2.name, member_names)
        self.assertNotIn(target3.name, member_names)

    def test_member_names(self):
        """
        Test the member_names function.
        """
        target1 = Database.create_target()
        target2 = Database.create_target()
        target3 = Database.create_target()
        group = Database.create_group('test_group')
        group.whitelist_member(target1)
        group.whitelist_member(target3)

        member_names = group.member_names

        self.assertIn(target1.name, member_names)
        self.assertIn(target3.name, member_names)
        self.assertNotIn(target2.name, member_names)

    def test_remove_member(self):
        """
        Test the remove_member function.
        """
        target1 = Database.create_target()
        target2 = Database.create_target()
        group = Database.create_group('test_group')
        group.whitelist_member(target1)
        group.whitelist_member(target2)
        group.remove_member(target2)

        member_names = group.member_names

        self.assertNotIn(target2.name, member_names)

    def test_whitelist_member(self):
        """
        Test the whitelist_member function.
        """
        group = Database.create_group('SOME GROUP')
        target = Database.create_target()
        group.whitelist_member(target)
        group = Database.get_group('SOME GROUP')
        self.assertListEqual([target.name], group.whitelist_members)

    def test_create(self):
        """
        Test to ensure a group can be properly created.
        """
        group = Database.create_group('TEST GROUP')
        self.assertEqual(group.name, 'TEST GROUP')

if __name__ == '__main__':
    unittest.main()
