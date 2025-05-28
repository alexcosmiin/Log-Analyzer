import unittest
from tests.common_functions import test_log, failThis

class TestOutputFormatting(unittest.TestCase):

    def test_output(self):
        test_log("Testing output formatting of test framework")
        try:
            test_log("Start test")
            test_log("Test passed")
        except Exception as e:
            failThis(f"Output formatting test failed: {e}")
