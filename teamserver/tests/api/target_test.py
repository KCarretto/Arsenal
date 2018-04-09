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
            'AA:BB:CC:DD:EE:FF',
            {'test_fact': 'hello'})

        self.assertEqual(False, data['error'])

        target = Database.get_target('TEST Target')
        self.assertIsNotNone(target)
        self.assertEqual(target.name, 'TEST Target')
        self.assertEqual('AA:BB:CC:DD:EE:FF', target.uuid)
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
        self.assertIsInstance(data['target']['uuid'], str)
        self.assertEqual(data['target']['uuid'], target.uuid)

    def test_get_params(self):
        """
        This test will pass if get returns the correct parameters.
        """
        target = Database.create_target('PARAMS TEST')
        action = Database.create_action(target.name)
        data = APIClient.get_target(self.client, 'PARAMS TEST', False, False, True)
        self.assertEqual(data['error'], False)
        self.assertIsInstance(data['target'], dict)
        self.assertEqual(data['target']['name'], 'PARAMS TEST')
        self.assertIsInstance(data['target']['uuid'], str)
        self.assertEqual(data['target']['uuid'], target.uuid)
        self.assertIsNotNone(data['target']['actions'])
        self.assertEqual(data['target']['actions'][0]['action_id'], action.action_id)
        with self.assertRaises(KeyError):
            data['target']['sessions'] #pylint: disable=pointless-statement
        with self.assertRaises(KeyError):
            data['target']['facts'] #pylint: disable=pointless-statement

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

        target = Database.create_target('FACT TEST', 'AA:BB:CC:DD:EE:FF', initial_facts)

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

    def test_target_rename(self):
        """
        Tests the RenameTarget API function.
        """
        target = Database.create_target('NOTTHIS')
        data = APIClient.rename_target(self.client, target.name, 'TEST')
        self.assertEqual(data['error'], False)
        target = Database.get_target('TEST')
        self.assertIsNotNone(target)
        self.assertEqual(target.name, 'TEST')
        with self.assertRaises(DoesNotExist):
            Database.get_target('NOTTHIS')

        target2 = Database.create_target()
        data = APIClient.rename_target(self.client, target2.name, 'TEST')
        self.assertEqual(data['error'], True)
        self.assertEqual(data['error_type'], 'cannot-rename-target')
        self.assertIsNotNone(Database.get_target(target2.name))

    def test_target_rename_association(self):
        """
        Tests the RenameTarget API function, check to make sure Sessions, Targets, and Groups.
        """
        target = Database.create_target()
        target_name = target.name
        session_id = Database.create_session(target_name).session_id
        orig_group = Database.create_group('some_group')
        orig_group.whitelist_member(target.name)
        action_id = Database.create_action(target_name).action_id

        data = APIClient.rename_target(self.client, target_name, 'TEST')
        self.assertEqual(data['error'], False)
        target = Database.get_target('TEST')
        self.assertIsNotNone(target)
        with self.assertRaises(DoesNotExist):
            Database.get_target(target_name)

        self.assertEqual(target.name, 'TEST')

        session = Database.get_session(session_id)
        self.assertEqual(session.target_name, 'TEST')

        action = Database.get_action(action_id)
        self.assertEqual(action.target_name, 'TEST')

        group = Database.get_group(orig_group.name)
        self.assertIn(target.name, group.members)

    def test_migrate_target(self):
        """
        Tests the MigrateTarget API function.
        """
        old_target = Database.create_target()
        old_sessions = [
            Database.create_session(old_target.name),
            Database.create_session(old_target.name),
            Database.create_session(old_target.name),
            Database.create_session(old_target.name),
            Database.create_session(old_target.name),
        ]
        new_target = Database.create_target(None, None, {'updated': True})

        new_sessions = [
            Database.create_session(new_target.name),
            Database.create_session(new_target.name),
            Database.create_session(new_target.name),
            Database.create_session(new_target.name),
            Database.create_session(new_target.name),
        ]
        data = APIClient.migrate_target(self.client, old_target.name, new_target.name)
        self.assertEqual(data['error'], False)

        # Ensure new_target has old name, and still has facts
        target = Database.get_target(old_target.name)
        self.assertIsNotNone(target)
        self.assertEqual(target.facts['updated'], True)

        # Ensure new target name is gone
        with self.assertRaises(DoesNotExist):
            Database.get_target(new_target.name)

        # Ensure all sessions exist on new_target
        self.assertListEqual(
            sorted([session.session_id for session in old_sessions+new_sessions]),
            sorted([session.session_id for session in target.sessions]))

if __name__ == '__main__':
    unittest.main()
