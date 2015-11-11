# coding: utf-8
import os
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

TEST_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'tests'
)

if __name__ == '__main__':
    suite = unittest.loader.TestLoader().discover(TEST_DIR)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit('Tests not passed')
