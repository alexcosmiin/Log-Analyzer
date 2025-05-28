import unittest
from tests.common_functions import test_log, failThis, expected_failure


class TestIntentionalFailure(unittest.TestCase):
    @expected_failure
    def test_fail_intentionally(self):
        test_log("This test is supposed to fail intentionally to check failure reporting")
        failThis("Intentional failure for testing the framework's failure detection")
