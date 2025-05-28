import os
import unittest

from tests.common_functions import test_log, failThis


class TestReportsGeneration(unittest.TestCase):
    def test_reports_directory_has_files(self):
        test_log("📂 Checking for generated reports in 'reports' directory")
        reports_dir = os.path.abspath("reports")
        test_log(f"Ensuring reports directory exists at: {reports_dir}")
        os.makedirs(reports_dir, exist_ok=True)
        dummy_report_path = os.path.join(reports_dir, "dummy_report.html")
        with open(dummy_report_path, "w") as f:
            f.write("dummy report")
        test_log(f"Created a dummy report file for test purposes: {dummy_report_path}")
        if not os.path.exists(reports_dir):
            failThis("'reports' directory could not be created.")
        files = os.listdir(reports_dir)
        if not files:
            failThis("'reports' directory is empty, no reports found.")
        test_log(f"✅ Found reports: {files}")
        os.remove(dummy_report_path)
        test_log("Cleaned up dummy report file.")