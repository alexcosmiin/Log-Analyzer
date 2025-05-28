import json
import os
import unittest

from tests.common_functions import test_log, failThis

class TestLogAnalysisAccuracy(unittest.TestCase):
    def test_log_analysis_correct_counts(self):
        test_log("📈 Verifying log analysis counts in output.json")

        output_path = os.path.abspath("output/output.json")
        if not os.path.exists(output_path):
            failThis("Output file does not exist for analysis.")

        with open(output_path, "r") as f:
            data = json.load(f)

        test_log("🔢 Checking counts of ERROR, WARNING, INFO entries")
        if data.get("ERROR", {}).get("count", 0) < 1:
            failThis("Expected at least 1 ERROR entry")

        if data.get("WARNING", {}).get("count", 0) < 2:
            failThis("Expected at least 2 WARNING entries")

        if data.get("INFO", {}).get("count", 0) < 3:
            failThis("Expected at least 3 INFO entries")

        test_log("✅ Log analysis counts are correct")
