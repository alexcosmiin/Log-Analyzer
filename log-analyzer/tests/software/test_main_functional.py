import unittest
from tests.common_functions import test_log, failThis, run_main_for_test


class TestMainFunctional(unittest.TestCase):
    def test_main_successful_run(self):
        test_log("Start test_main_successful_run using helper")

        sample_log_lines = [
            "Critical failure happened",
            "Error: something went wrong",
            "Info: all good"
        ]

        exit_code, output_json, used_log_path, _ = run_main_for_test(
            log_content_lines=sample_log_lines
        )

        if exit_code != 0:
            failThis(f"main() was expected to exit with 0, but got {exit_code}")

        if output_json is None:
            failThis("Output JSON was not created or was unparsable by helper.")
            return

        test_log("Verifying JSON output for CRITICAL, ERROR, INFO, and metadata keys.")
        expected_keys = ["CRITICAL", "ERROR", "INFO", "metadata"]
        for key in expected_keys:
            if key not in output_json:
                failThis(f"Output JSON missing expected key: {key}. Found keys: {list(output_json.keys())}")

        if output_json.get("CRITICAL", {}).get("count") != 1:
            failThis("CRITICAL count incorrect.")
        if output_json.get("ERROR", {}).get("count") != 1:
            failThis("ERROR count incorrect.")
        if output_json.get("INFO", {}).get("count") != 1:
            failThis("INFO count incorrect.")

        metadata = output_json.get("metadata", {})
        if metadata.get("total_lines_processed") != len(sample_log_lines):
            failThis(
                f"Expected 'total_lines_processed' to be {len(sample_log_lines)}, got {metadata.get('total_lines_processed')}.")
        if metadata.get("log_file_path") != used_log_path:
            failThis(f"Expected log_file_path in metadata to be {used_log_path}, got {metadata.get('log_file_path')}")

        test_log("All expected keys and counts found in output JSON.")
