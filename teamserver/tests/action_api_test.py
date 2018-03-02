"""
    This module tests basic functionality of the action API.
"""
import os
import sys
import unittest

from flask import json
from testutils import ModelTest, create_test_action, get_action #pylint: disable=no-name-in-module

# Configure path to include teamserver module
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from teamserver.config import ACTION_TYPES, ACTION_STATUSES #pylint: disable=wrong-import-position

class ActionAPITest(ModelTest):
    """
    This class is used to test the Action API funcitons.
    """
    def test_create(self):
        """
        This test will pass if the action is created and content matches.
        """
        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateAction',
                target_name='ACTION TEST Target',
                action_string='exec ls -al /dir'
            )),
            content_type='application/json',
            follow_redirects=True
        )

        data = json.loads(resp.data)
        action_id = data['action_id']

        self.assertEqual(False, data['error'])
        action = get_action(action_id)
        self.assertIsNotNone(action)
        self.assertEqual(action.action_type, ACTION_TYPES.get('exec', 1))
        self.assertEqual(action.command, 'ls')
        self.assertListEqual(action.args, ['-al', '/dir'])

    def test_get(self):
        """
        This test will pass if it finds the correct action.
        """
        action = create_test_action('TEST TARGET', 'exec ls')
        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='GetAction',
                action_id=action.action_id,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(resp.data)
        self.assertEqual(data['error'], False)
        self.assertIsNotNone(data['action'])
        self.assertEqual(action.action_id, data['action']['action_id'])
        self.assertEqual(action.target_name, data['action']['target_name'])
        self.assertEqual(data['action']['command'], 'ls')

    def test_cancel(self):
        """
        This test will pass if an action is successfully cancelled.
        """
        action = create_test_action('TEST TARGET', 'exec echo hello world')
        self.assertEqual(action.cancelled, False)
        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='CancelAction',
                action_id=action.action_id,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(resp.data)
        self.assertEqual(data['error'], False)

        action = get_action(action)
        self.assertEqual(action.status, ACTION_STATUSES.get('cancelled'))
        self.assertEqual(action.cancelled, True)

if __name__ == '__main__':
    unittest.main()
