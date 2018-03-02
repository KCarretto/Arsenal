"""
    This module tests basic functionality of the target model.
    It does not test any database connectivity, but it does
    utilize mongoengine's mock database implementation.
"""
import unittest

from flask import json
from testutils import ModelTest, create_test_session, create_test_target, get_session #pylint: disable=no-name-in-module

class SessionAPITest(ModelTest):
    """
    This class is used to test the Session API funcitons.
    """
    def test_create(self):
        """
        This test will pass if the session is created.
        """
        target = create_test_target()
        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateSession',
                mac_addrs=target.mac_addrs,
                servers=['10.10.10.10', 'https://google.com'],
                interval=120,
                interval_delta=20,
                config_dict={'TEST_SESSION': 'hello world'},
            )),
            content_type='application/json',
            follow_redirects=True
        )

        data = json.loads(resp.data)
        session_id = data['session_id']

        self.assertEqual(False, data['error'])
        self.assertIsNotNone(get_session(session_id))

    def test_get(self):
        """
        This test will pass if it finds the correct session.
        """
        session = create_test_session()
        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='GetSession',
                session_id=session.session_id,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(resp.data)
        session_id = data['session']['session_id']
        self.assertEqual(session_id, session.session_id)

    def test_update_config(self):
        """
        This test will pass if the config is correctly set.
        """
        initial_config = {
            'some fact': 54,
            'some other fact': 'Pi',
            'A list fact': ['sdasd', 'asdasd']
        }

        target = create_test_target()
        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateSession',
                mac_addrs=target.mac_addrs,
                config_dict=initial_config
            )),
            content_type='application/json',
            follow_redirects=True
            )
        data = json.loads(resp.data)
        self.assertEqual(False, data['error'])

        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='UpdateSessionConfig',
                session_id=data['session_id'],
                servers=['10.10.10.10'],
                interval=10,
                interval_delta=5,
                config_dict={
                    'new fact': 'Wow. I am new!',
                    'A list fact': ['asdasd', 'sdasd'],
                    'some fact': 55
                },
            )),
            content_type='application/json',
            follow_redirects=True
            )

        final_config = {
            'interval': 10,
            'interval_delta': 5,
            'servers': ['10.10.10.10'],
            'new fact': 'Wow. I am new!',
            'some other fact': 'Pi',
            'A list fact': ['asdasd', 'sdasd'],
            'some fact': 55
        }

        data = json.loads(resp.data)
        self.assertEqual(final_config, data['config'])

    def test_list(self):
        """
        Populates the database with sample targets, and calls the list API
        function to ensure that all are returned.
        """
        sessions = [
            create_test_session('a'),
            create_test_session('b'),
            create_test_session('c'),
            create_test_session('d'),
            create_test_session('e'),
        ]
        resp = self.client.post(
            '/api',
            data=json.dumps(dict(
                method='ListSessions',
            )),
            content_type='application/json',
            follow_redirects=True
            )
        data = json.loads(resp.data)
        self.assertEqual(
            sorted(list(data['sessions'].keys())),
            sorted([session.session_id for session in sessions])
            )

if __name__ == '__main__':
    unittest.main()
