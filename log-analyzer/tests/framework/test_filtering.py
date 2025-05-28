import unittest
from tests.common_functions import test_log, failThis
from run_tests import run_tests

class TestFiltering(unittest.TestCase):

    def test_filter_by_name(self):
        filter_string = "test_dummy_pass"
        test_log(f"Testing filtering by test name containing '{filter_string}'")
        results = run_tests(filter_str=filter_string)
        if results['total'] == 0:
            failThis(f"No tests found matching filter '{filter_string}'")
        if results['total'] != 1:
            failThis(f"Expected 1 test for filter '{filter_string}', but found {results['total']}")
        test_log(f"Found {results['total']} test(s) matching filter '{filter_string}'")

    def test_filter_by_category(self):
        category = "dummy"
        test_log(f"Testing filtering by category '{category}'")
        results = run_tests(category=category)
        if results['total'] == 0:
            failThis(f"No tests found for category '{category}'")
        if results['total'] != 1:
            failThis(f"Expected 1 test in category '{category}', but found {results['total']}")
        test_log(f"Found {results['total']} test(s) in category '{category}'")