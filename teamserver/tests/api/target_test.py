"""
    This module tests basic functionality of the target API.
"""
import sys
import unittest

from mongoengine import DoesNotExist

try:
    from testutils import BaseTest, Database, APIClient
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils import BaseTest, Database, APIClient

class TargetAPITest(BaseTest):
    """
    This class is used to test the Target API functions.
    """
    def test_create(self):
        """
        This test will pass if the target is created.
        """

        with self.assertRaises(DoesNotExist):
            Database.get_target('TEST Target')

        data = APIClient.create_target(
            self.client,
            'TEST Target',
            ['AA:BB:CC:DD:EE:FF'],
            {'test_fact': 'hello'})

        self.assertEqual(False, data['error'])

        target = Database.get_target('TEST Target')
        self.assertIsNotNone(target)
        self.assertEqual(target.name, 'TEST Target')
        self.assertListEqual(['AA:BB:CC:DD:EE:FF'], target.mac_addrs)
        self.assertDictEqual({'test_fact': 'hello'}, target.facts)

    def test_get(self):
        """
        This test will pass if it finds the correct target.
        """
        target = Database.create_target('GET TEST')
        data = APIClient.get_target(self.client, 'GET TEST')
        self.assertEqual(data['error'], False)
        self.assertIsInstance(data['target'], dict)
        self.assertEqual(data['target']['name'], 'GET TEST')
        self.assertIsInstance(data['target']['mac_addrs'], list)
        self.assertListEqual(data['target']['mac_addrs'], target.mac_addrs)

    def test_target_set_facts(self):
        """
        This test will pass if the facts are correctly set.
        """
        initial_facts = {
            'some fact': 54,
            'some other fact': 'Pi',
            'A list fact': ['sdasd', 'asdasd']
        }
        fact_update = {
            'new fact': 'Wow. I am new!',
            'A list fact': ['asdasd', 'sdasd'],
            'some fact': 55
        }
        final_facts = {
            'new fact': 'Wow. I am new!',
            'some other fact': 'Pi',
            'A list fact': ['asdasd', 'sdasd'],
            'some fact': 55
        }

        target = Database.create_target('FACT TEST', ['AA:BB:CC:DD:EE:FF'], initial_facts)

        data = APIClient.set_target_facts(self.client, 'FACT TEST', fact_update)
        self.assertEqual(data['error'], False)

        target = Database.get_target('FACT TEST')
        self.assertIsNotNone(target)
        self.assertDictEqual(final_facts, target.facts)

    def test_target_list(self):
        """
        Populates the database with sample targets, and calls the list API
        function to ensure that all are returned.
        """
        targets = [
            Database.create_target(),
            Database.create_target(),
            Database.create_target(),
            Database.create_target(),
        ]

        data = APIClient.list_targets(self.client)
        self.assertEqual(data['error'], False)

        self.assertListEqual(
            sorted(list(data['targets'].keys())),
            sorted([target.name for target in targets]))

    def test_target_groups(self):
        """
        Tests the GetTargetGroups API function.
        """
        target = Database.create_target()
        groups = [
            Database.create_group(),
            Database.create_group(),
            Database.create_group(),
            Database.create_group(),
        ]
        for group in groups:
            group.whitelist_member(target)

        data = APIClient.get_target_groups(self.client, target.name)
        self.assertEqual(data['error'], False)
        self.assertListEqual(
            sorted([group.name for group in groups]),
            sorted(data['groups'])
        )

if __name__ == '__main__':
    unittest.main()
