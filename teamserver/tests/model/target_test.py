"""
    This module tests basic functionality of the target model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import sys
import unittest

from mongoengine import NotUniqueError, DoesNotExist

# pylint: disable=duplicate-code
try:
    from testutils.test_cases import BaseTest
    from testutils.database import Database
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils.test_cases import BaseTest
    from tests.testutils.database import Database

class TargetModelTest(BaseTest):
    """
    This class is used to test the teamserver's target model class.
    """
    TEST_NAME = 'test_target'
    TEST_FACTS = {
        'some_fact': 'correct',
        'a list': ['hello'],
        'a_dict': {
            'simple': 'dict'
        },
        'a_complex_list': [
            {
                'embedded': 'dict'
            }
        ],
        'a_complex_dict': {
            'some stuff': {
                'whoa': [5, 4, 23]
            }
        }
    }

    def test_create_pass(self):
        """
        This test will attempt to create a target model object.
        """
        target = Database.create_target(self.TEST_NAME, None, self.TEST_FACTS)
        self.assertEqual(target.name, self.TEST_NAME)
        self.assertEqual(target.facts, self.TEST_FACTS)

    def test_find_pass(self):
        """
        This test will attempt to create a target model object,
        save it to the database, and then find it.
        """
        target1 = Database.create_target(self.TEST_NAME)
        target2 = Database.get_target(self.TEST_NAME)
        self.assertEqual(target1, target2)

    def test_create_dup_name_fail(self):
        """
        This test will attempt to create two targets with identitical names,
        and it will fail as Mongo should throw a not unique exception.
        """
        with self.assertRaises(NotUniqueError):
            target1 = Database.create_target(self.TEST_NAME)
            target2 = Database.create_target(self.TEST_NAME)
            self.assertEqual(target1.name, target2.name)

    def test_create_dup_macs_fail(self):
        """
        This test will attempt to create targets with the same mac_addrs,
        and it will fail as mongo should throw a not unique exception.
        """

        # Single element, same order
        with self.assertRaises(NotUniqueError):
            target1 = Database.create_target(None, ['AA:BB:CC:DD:EE:FF'])
            target2 = Database.create_target(None, ['AA:BB:CC:DD:EE:FF'])
            self.assertEqual(target1.mac_addrs, target2.mac_addrs)

        # Multi element, same order
        with self.assertRaises(NotUniqueError):
            target1 = Database.create_target(None, [
                'AA:BB:CC:DD:EE:FF',
                'AA:BB:CC:DD:EE:AA'])
            target2 = Database.create_target(None, [
                'AA:BB:CC:DD:EE:FF',
                'AA:BB:CC:DD:EE:AA'])
            self.assertEqual(target1.mac_addrs, target2.mac_addrs)

        # Multi element, different order
        with self.assertRaises(NotUniqueError):
            target1 = Database.create_target(None, [
                'AA:BB:CC:DD:EE:FF',
                'AA:BB:CC:DD:EE:AA'])
            target2 = Database.create_target(None, [
                'AA:BB:CC:DD:EE:AA',
                'AA:BB:CC:DD:EE:FF'])
            self.assertEqual(target1.mac_addrs, target2.mac_addrs)

        # Multi element, different order, different encoding
        with self.assertRaises(NotUniqueError):
            target1 = Database.create_target(None, [
                'AA:BB:CC:DD:EE:FF'.encode('utf-8'),
                'AA:BB:CC:DD:EE:AA'])
            target2 = Database.create_target(None, [
                'AA:BB:CC:DD:EE:AA',
                'AA:BB:CC:DD:EE:FF'.encode('ascii')])
            self.assertEqual(target1.mac_addrs, target2.mac_addrs)

    def test_find_no_name_fail(self):
        """
        This target tests to ensure mongoengine throws an error if the target
        is not found by name.
        """
        with self.assertRaises(DoesNotExist):
            Database.get_target('HI. I DONT EXIST.')

if __name__ == '__main__':
    unittest.main()
