from test_framework.core.test_case import TestCase
from test_framework.utils import step
from test_framework.utils.assertions import Assertions


class SmokeTest(TestCase):
    """Basic smoke tests to verify the testing framework works"""

    @step("Basic truth assertion")
    def test_truth(self):
        """The simplest possible test that should always pass"""
        with self.add_step("Verify basic truth"):
            Assertions.assert_true(True, "This should always be true")

        with self.add_step("Verify basic math"):
            Assertions.assert_equal(1 + 1, 2, "Basic math should work")

    @step("Basic string operations")
    def test_strings(self):
        """Test basic string operations"""
        with self.add_step("Create test string"):
            test_string = "hello"

        with self.add_step("Verify string length"):
            Assertions.assert_equal(len(test_string), 5)

        with self.add_step("Verify string content"):
            Assertions.assert_contains("hell", test_string)