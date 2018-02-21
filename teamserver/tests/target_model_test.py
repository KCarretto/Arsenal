"""
    This module tests basic functionality of the target model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import sys
import os
import unittest

# Configure path to include teamserver module
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

import teamserver #pylint: disable=wrong-import-position
from teamserver.models.target  import Target #pylint: disable=wrong-import-position

def create_test_app():
    """
    This function creates the flask application with test values.
    """
    return teamserver.create_app(
        TESTING=True,
        MONGODB_SETTINGS=
        {
            'db': 'arsenal_default',
            'host': 'mongomock://localhost'
        })

class TargetModelTest(unittest.TestCase):
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

    def setUp(self):
        """
        This performs test setup operations.
        """
        self.test_app = create_test_app()
        self.test_app.testing = True
        self.client = self.test_app.test_client()

    def test_pass(self):
        """
        This test should always pass.
        """
        pass

    def test_create_pass(self):
        """
        This test will attempt to create a target model object.
        """
        target = Target(
            name=self.TEST_NAME,
            facts=self.TEST_FACTS,
            group_names=self.TEST_GROUPS,
        )
        self.assertEqual(target.name, self.TEST_NAME)
        self.assertEqual(target.facts, self.TEST_FACTS)
        self.assertEqual(target.group_names, self.TEST_GROUPS)

    def test_create_pass_find(self):
        """
        This test will attempt to create a target model object,
        save it to the database, and then find it.
        """
        target1 = Target(
            name=self.TEST_NAME,
            facts=self.TEST_FACTS
        )
        target1.save()
        target2 = Target.objects.get(name=self.TEST_NAME) #pylint: disable=no-member
        self.assertEqual(target1, target2)


if __name__ == '__main__':
    unittest.main()

