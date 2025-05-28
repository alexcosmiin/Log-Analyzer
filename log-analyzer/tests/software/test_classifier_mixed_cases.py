from src.classifier import classify_log_line
from tests.common_functions import test_log, failThis
import unittest

class TestClassifierMixedCases():
    def test_classifier_mixed_log_entries(self):
        test_log("Start test_classifier_mixed_log_entries")
        test_cases = {
            "System CRITICAL failure occurred": "CRITICAL",
            "This is a debug trace": "DEBUG",
            "INFO: User logged in": "INFO",
            "WARNING: High memory usage": "WARNING",
            "Something failed unexpectedly": "FAILED",
            "Generic ERROR detected": "ERROR",
            "Just a line with no keyword": "UNKNOWN"
        }

        for line, expected in test_cases.items():
            result = classify_log_line(line)
            if result != expected:
                failThis(f"Line: '{line}' classified as {result}, expected {expected}")
