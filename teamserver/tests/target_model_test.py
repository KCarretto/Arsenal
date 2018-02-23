"""
    This module tests basic functionality of the target model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import unittest

from mongoengine import NotUniqueError
from testutils import ModelTest, create_test_target, get_target #pylint: disable=no-name-in-module

class TargetModelTest(ModelTest):
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
    TEST_GROUPS = ["group_a", "group_b"]

    def test_create_pass(self):
        """
        This test will attempt to create a target model object.
        """
        target = create_test_target(self.TEST_NAME, self.TEST_GROUPS, self.TEST_FACTS)
        self.assertEqual(target.name, self.TEST_NAME)
        self.assertEqual(target.facts, self.TEST_FACTS)
        self.assertEqual(target.group_names, self.TEST_GROUPS)

    def test_create_find_pass(self):
        """
        This test will attempt to create a target model object,
        save it to the database, and then find it.
        """
        target1 = create_test_target(self.TEST_NAME)
        target2 = get_target(self.TEST_NAME)
        self.assertEqual(target1, target2)

    def test_create_dup_name_fail(self):
        """
        This test will attempt to create two targets with identitical names,
        and it will fail as Mongo should throw a not unique exception.
        """
        with self.assertRaises(NotUniqueError):
            target1 = create_test_target(self.TEST_NAME)
            target2 = create_test_target(self.TEST_NAME)
            self.assertEqual(target1, target2)

if __name__ == '__main__':
    unittest.main()
