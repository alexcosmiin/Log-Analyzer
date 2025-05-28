import unittest
from tests.common_functions import test_log
from run_tests import run_tests

class TestNoTestsFound(unittest.TestCase):

    def test_no_tests_found(self):
        test_log("Testing behavior when no tests match the filter")
        results = run_tests(filter_str="non_existent_test_name_123")
        if results['total'] != 0:
            test_log(f"Unexpected tests found: {results['total']}")
        else:
            test_log("No tests found as expected")
