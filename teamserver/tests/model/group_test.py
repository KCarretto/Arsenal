"""
    This module tests basic functionality of the group model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import sys
import unittest

try:
    from testutils.test_cases import ModelTest
    from testutils.database import Database
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils.test_cases import ModelTest
    from tests.testutils.database import Database

class GroupModelTest(ModelTest):
    """
    This class is used to test the teamserver's group model class.
    """
    def test_create(self):
        """
        Test to ensure a group can be properly created.
        """
        group = Database.create_group('TEST GROUP')
        self.assertEqual(group.name, 'TEST GROUP')

if __name__ == '__main__':
    unittest.main()
