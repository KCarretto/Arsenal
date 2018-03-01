"""
    This module tests basic functionality of the target model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import unittest

from flask import json
from mongoengine import DoesNotExist
from testutils import ModelTest, create_test_target, get_target #pylint: disable=no-name-in-module

class TargetAPITest(ModelTest):
    """
    This class is used to test the Target API funcitons.
    """
    def test_create(self):
        """
        This test will pass if the target is created.
        """
        with self.assertRaises(DoesNotExist):
            get_target('TEST Target')

        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateTarget',
                name='TEST Target',
                mac_addrs=['AA:BB:CC:DD:EE:FF']
            )),
            content_type='application/json',
            follow_redirects=True
            )

        data = json.loads(resp.data)
        self.assertEqual(False, data['error'])
        self.assertIsNotNone(get_target('TEST Target'))

    def test_get(self):
        """
        This test will pass if it finds the correct target.
        """
        create_test_target('GET TEST')
        self.assertIsNotNone(get_target('GET TEST'))
        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='GetTarget',
                name='GET TEST',
            )),
            content_type='application/json',
            follow_redirects=True
            )
        data = json.loads(resp.data)
        self.assertEqual(False, data['error'])
        self.assertEqual('GET TEST', data['target']['name'])

    def test_target_set_facts(self):
        """
        This test will pass if the facts are correctly set.
        """
        initial_facts = {
            'some fact': 54,
            'some other fact': 'Pi',
            'A list fact': ['sdasd', 'asdasd']
        }

        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateTarget',
                name='TEST Target',
                mac_addrs=['AA:BB:CC:DD:EE:FF'],
                facts=initial_facts,
            )),
            content_type='application/json',
            follow_redirects=True
            )
        data = json.loads(resp.data)
        self.assertEqual(False, data['error'])

        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='SetTargetFacts',
                name='TEST Target',
                mac_addrs=['AA:BB:CC:DD:EE:FF'],
                facts={
                    'new fact': 'Wow. I am new!',
                    'A list fact': ['asdasd', 'sdasd'],
                    'some fact': 55
                },
            )),
            content_type='application/json',
            follow_redirects=True
            )

        final_facts = {
            'new fact': 'Wow. I am new!',
            'some other fact': 'Pi',
            'A list fact': ['asdasd', 'sdasd'],
            'some fact': 55
        }

        data = json.loads(resp.data)
        self.assertEqual(final_facts, data['target']['facts'])

    def test_target_list(self):
        """
        Populates the database with sample targets, and calls the list API
        function to ensure that all are returned.
        """
        create_test_target('a')
        create_test_target('b')
        create_test_target('c')
        create_test_target('d')

        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='ListTargets',
            )),
            content_type='application/json',
            follow_redirects=True
            )
        data = json.loads(resp.data)
        self.assertEqual(list(data['targets'].keys()), ['a','b','c','d'])

if __name__ == '__main__':
    unittest.main()
