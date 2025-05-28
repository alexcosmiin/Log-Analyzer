import unittest
from tests.common_functions import test_log, failThis

class TestExceptionHandling(unittest.TestCase):

    def test_exception_propagation(self):
        test_log("Testing exception handling")

        def test_func():
            raise ValueError("Test exception")

        try:
            test_func()
        except Exception:
            test_log("Exception correctly propagated")
        else:
            failThis("Exception inside test was not raised")
