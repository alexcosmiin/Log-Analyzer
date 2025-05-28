import unittest
from tests.common_functions import test_log, failThis, expected_failure


class TestMultipleFailures(unittest.TestCase):
    @expected_failure
    def test_fail1(self):
        test_log("Triggering first intentional failure")
        failThis("Failure 1")

    @expected_failure
    def test_fail2(self):
        test_log("Triggering second intentional failure")
        failThis("Failure 2")

    def test_pass(self):
        test_log("This test passes without failure")
