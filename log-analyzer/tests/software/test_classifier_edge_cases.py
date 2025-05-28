from src.classifier import classify_log_line
from tests.common_functions import failThis, test_log
import unittest

class TestClassifierEdgeCases(unittest.TestCase):
    def test_classifier_edge_case_empty_and_spaces(self):
        test_log("Start test_classifier_edge_case_empty_and_spaces")
        try:
            assert classify_log_line("") == "UNKNOWN"
            assert classify_log_line("    ") == "UNKNOWN"
            assert classify_log_line("\n") == "UNKNOWN"
        except AssertionError:
            failThis("classify_log_line failed on empty or whitespace strings")

    def test_classifier_case_insensitivity_and_partial_words(self):
        test_log("Start test_classifier_case_insensitivity_and_partial_words")
        try:
            assert classify_log_line("CRITICAl error") == "CRITICAL"
            assert classify_log_line("error occurred") == "ERROR"
            assert classify_log_line("failed login") == "FAILED"
            # Substrings that should NOT match exactly
            assert classify_log_line("fail") == "UNKNOWN"
            assert classify_log_line("warn") == "UNKNOWN"
        except AssertionError:
            failThis("classify_log_line failed on case or partial words")

