from src.classifier import classify_log_line
from tests.common_functions import failThis, test_log
import unittest


class TestClassifier(unittest.TestCase):
    def test_classify_known_levels(self):
        test_log("Start test_classify_known_levels")

        try:
            assert classify_log_line("Critical error occurred") == "CRITICAL"
            assert classify_log_line("ERROR: Something failed") == "ERROR"
            assert classify_log_line("User login failed") == "FAILED"
            assert classify_log_line("Warning: Disk almost full") == "WARNING"
            assert classify_log_line("Info: Process started") == "INFO"
            assert classify_log_line("Debug mode enabled") == "DEBUG"
        except AssertionError:
            failThis("classify_log_line did not classify known levels correctly")


    def test_classify_unknown(self):
        test_log("Start test_classify_unknown")
        try:
            assert classify_log_line("This is some random log entry") == "UNKNOWN"
            assert classify_log_line("") == "UNKNOWN"
        except AssertionError:
            failThis("classify_log_line failed to classify unknown entries")


