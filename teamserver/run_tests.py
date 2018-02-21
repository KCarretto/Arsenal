"""
    This module will run all unit test cases.
"""
import unittest

LOADER = unittest.TestLoader()
SUITE = LOADER.discover('tests/', pattern='*_test.py')

RUNNER = unittest.TextTestRunner()
RUNNER.run(SUITE)
