# NOTE: Logging now uses flask app logger

# """
#     This module tests basic functionality of the log API.
# """
# from uuid import uuid4

# import sys
# import time
# import unittest

# try:
#     from testutils import BaseTest, Database, APIClient
# except ModuleNotFoundError:
#     # Configure path to start at teamserver module
#     from os.path import dirname, abspath
#     sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
#     from tests.testutils import BaseTest, Database, APIClient

# class LogAPITest(BaseTest):
#     """
#     This class is used to test the Log API functions.
#     """
#     def test_create(self):
#         """
#         Test the CreateLog API function.
#         """
#         app = 'TEST APP {}'.format(uuid4())
#         data = APIClient.create_log(
#             self.client,
#             'TEST APP',
#             'FATAL',
#             'Testing CreateLog API method'
#         )
#         self.assertEqual(data['error'], False)

#         for entry in Database.list_logs(app):
#             self.assertEqual(entry.message, 'Testing CreateLog API method')

#     def test_list(self):
#         """
#         Test the ListLogs API function.
#         """
#         Database.create_log(0, 'NOSEE', 'FATAL', 'NOSEE')
#         Database.create_log(time.time(), 'WESEE', 'FATAL', 'WESEE')
#         archived_log = Database.create_log(time.time(), 'ARCHIVED', 'FATAL', 'ARCHIVED')
#         archived_log.archived = True
#         archived_log.save()

#         for entry in APIClient.list_logs(self.client, False, 10)['logs']:
#             self.assertNotEqual(entry['application'], 'NOSEE')
#             self.assertNotEqual(entry['application'], 'ARCHIVED')

#         logs = [entry['application'] for entry in APIClient.list_logs(self.client, True)['logs']]
#         self.assertIn('NOSEE', logs)
#         self.assertIn('ARCHIVED', logs)


# if __name__ == '__main__':
#     unittest.main()
