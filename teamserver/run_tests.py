"""
    This module will run all unit test cases.
"""
import sys
import unittest

LOADER = unittest.TestLoader()
SUITE = LOADER.discover('tests/', pattern='*_test.py')

RUNNER = unittest.TextTestRunner()
ret = not RUNNER.run(SUITE).wasSuccessful()
sys.exit(ret)
