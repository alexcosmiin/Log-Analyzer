import json
import os
import unittest
from tests.common_functions import test_log, failThis

class TestOutputJSONStructure(unittest.TestCase):
    def test_json_structure_validity(self):
        test_log("📊 Validating output.json structure")

        output_file = os.path.abspath("output/output.json")
        if not os.path.exists(output_file):
            failThis("output.json file does not exist for structure validation.")

        with open(output_file) as f:
            data = json.load(f)

        test_log(f"ℹ️ JSON keys found: {list(data.keys())}")

        expected_keys = ["ERROR", "WARNING", "INFO"]
        for key in expected_keys:
            if key not in data:
                failThis(f"Missing expected key '{key}' in output.json")

        test_log("✅ JSON structure validated successfully")
