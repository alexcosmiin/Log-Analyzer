import os
import unittest
from tests.common_functions import test_log, failThis

class TestOutputFile(unittest.TestCase):
    def test_output_json_file_created(self):
        test_log("📁 Checking if output JSON file exists")

        output_file = os.path.abspath("output/output.json")
        if not os.path.exists(output_file):
            failThis("output.json file was not created.")

        test_log("✅ output.json file exists")
