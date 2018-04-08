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
    from teamserver.models import Group, GroupAutomemberRule
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils import BaseTest, Database
    from teamserver.models import Group, GroupAutomemberRule

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

        group1.whitelist_member(target.name)
        group2.whitelist_member(target.name)
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
        group.whitelist_member(target1.name)
        group.whitelist_member(target2.name)

        member_names = group.members

        self.assertIn(target1.name, member_names)
        self.assertIn(target2.name, member_names)
        self.assertNotIn(target3.name, member_names)

    def test_remove_member(self):
        """
        Test the remove_member function.
        """
        target1 = Database.create_target()
        target2 = Database.create_target()
        group = Database.create_group('test_group')
        group.whitelist_member(target1.name)
        group.whitelist_member(target2.name)
        group.remove_member(target2.name)

        self.assertNotIn(target2.name, group.members)

    def test_whitelist_member(self):
        """
        Test the whitelist_member function.
        """
        group = Database.create_group('SOME GROUP')
        target = Database.create_target()
        group.whitelist_member(target.name)
        group = Database.get_group('SOME GROUP')
        self.assertListEqual([target.name], group.whitelist_members)

    def test_group_rules(self):
        """
        Test if group Automember rules are functioning as expected.
        """
        group = Database.create_group()
        targets = [
            Database.create_target(None, None, {'include': 'yes'}),
            Database.create_target(None, None, {'something': {'cool': True}}),
            Database.create_target(None, None, {'interfaces': [
                {'name': 'eth0', 'ip_addrs': ['192.168.1.1', '127.0.0.1']}]}),
            Database.create_target(None, None, {
                'include': 'sureyessure',
                'something': {'cool': False}}),
        ]
        group.membership_rules = [
            Database.create_group_rule(
                attribute='facts.include', regex='.*yes.*'),
            Database.create_group_rule(
                attribute='facts.something.cool', regex='True'),
            Database.create_group_rule(
                attribute='facts.interfaces', regex='.*192.168.1.*'),
        ]
        group.save()

        for target in targets:
            self.assertIn(target.name, group.members)

    def test_create(self):
        """
        Test to ensure a group can be properly created.
        """
        group = Database.create_group('TEST GROUP')
        self.assertEqual(group.name, 'TEST GROUP')

if __name__ == '__main__':
    unittest.main()
