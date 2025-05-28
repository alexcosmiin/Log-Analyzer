import unittest
from tests.common_functions import test_log, failThis

class TestTestLogOutputCaptured(unittest.TestCase):

    def test_log_output(self):
        test_log("Testing test_log() output capture")
        try:
            test_log("This is a test message")
        except Exception as e:
            failThis(f"test_log() raised an exception: {e}")
