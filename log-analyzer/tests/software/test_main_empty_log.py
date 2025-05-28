import unittest
from tests.common_functions import test_log, failThis, run_main_for_test


class TestMainEmptyLog(unittest.TestCase):
    def test_main_with_empty_log(self):
        test_log("Start test_main_with_empty_log using NEW helper")

        exit_code, output_json, used_log_path, _ = run_main_for_test(
            log_content_lines=[]
        )

        if exit_code != 0:
            failThis(f"main() should return 0 for an empty log file, but got {exit_code}")
        test_log("main() returned 0 as expected.")

        if output_json is None:
            failThis("Output JSON was not created or was unparsable.")

        metadata = output_json.get("metadata", {})
        if metadata.get("total_lines_processed") != 0:
            failThis(f"Expected 'total_lines_processed' to be 0, got {metadata.get('total_lines_processed')}.")

        if metadata.get("log_file_path") != used_log_path:
            failThis(f"Expected log_file_path in metadata to be {used_log_path}, got {metadata.get('log_file_path')}")

        test_log("Test finished successfully.")