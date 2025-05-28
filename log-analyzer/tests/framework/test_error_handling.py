import unittest
from tests.common_functions import test_log, failThis

class TestErrorHandling(unittest.TestCase):

    def test_unexpected_exception(self):
        test_log("Testing handling of unexpected exceptions")

        try:
            raise ZeroDivisionError("divide by zero")
        except ZeroDivisionError:
            test_log("Caught ZeroDivisionError as expected")
        except Exception as e:
            failThis(f"Unexpected exception caught: {e}")
        else:
            failThis("Expected exception was not raised")

        test_log("Unexpected exception handling test completed successfully")
