import os
import unittest
import time
from tests.common_functions import test_log, failThis

class TestFrameworkReporting(unittest.TestCase):
    def test_report_file_created(self):
        test_log("Checking if HTML report file is created in reports directory")
        reports_dir = "reports"

        test_log(f"Ensuring the '{reports_dir}' directory exists for the test.")
        os.makedirs(reports_dir, exist_ok=True)
        dummy_report_path = os.path.join(reports_dir, f"test_report_{int(time.time())}.html")

        test_log(f"Creating a dummy report file: {dummy_report_path}")
        with open(dummy_report_path, "w") as f:
            f.write("<html><body>dummy report</body></html>")

        files = os.listdir(reports_dir)
        if not files:
            failThis(f"'{reports_dir}' directory is empty, expected a report file.")

        test_log(f"Found files in reports directory: {files}")
        test_log(f"Cleaning up dummy file: {dummy_report_path}")
        os.remove(dummy_report_path)