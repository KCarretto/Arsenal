"""
A test to make sure that logging is working properly.
"""
import sys
import unittest

try:
    from testutils import BaseTest
    from teamserver.config import LOG_LEVEL
    from teamserver.models import log, Log
except ModuleNotFoundError:
    # Configure path to start at teamserver module
    from os.path import dirname, abspath
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from tests.testutils import BaseTest
    from teamserver.config import LOG_LEVEL
    from teamserver.models import log, Log

class LogTest(BaseTest):
    """
    This class is used to test the teamserver's internal logging ability.
    """
    def test_log(self):
        """
        This test will attempt to create a log.
        """
        log(LOG_LEVEL, 'Internal Logging Test')
        self.assertEqual(len(Log.list()), 1)

if __name__ == '__main__':
    unittest.main()
