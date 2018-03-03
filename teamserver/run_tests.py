"""
    This module will run all unit test cases.
"""
import sys
import unittest

def main():
    """
    Discover and run unit tests.
    """
    loader = unittest.TestLoader()
    suite = loader.discover('tests/', pattern='*_test.py')

    runner = unittest.TextTestRunner()
    ret = not runner.run(suite).wasSuccessful()
    sys.exit(ret)

if __name__ == '__main__':
    main()
