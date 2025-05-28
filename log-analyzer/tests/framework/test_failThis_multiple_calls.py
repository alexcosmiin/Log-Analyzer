import unittest
from tests.common_functions import test_log, failThis, expected_failure


class TestFailThisMultipleCalls(unittest.TestCase):
    @expected_failure
    def test_multiple_fail_calls(self):
        test_log("Calling failThis first time")
        try:
            failThis("First failure")
        except Exception as e:
            test_log(f"Caught first failure: {e}")

        test_log("Calling failThis second time")
        try:
            failThis("Second failure - should be ignored or handled gracefully")
        except Exception as e:
            test_log(f"Caught second failure: {e}")
