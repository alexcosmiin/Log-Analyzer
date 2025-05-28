import unittest
from tests.common_functions import test_log, failThis, run_main_for_test


class TestMainOutputStructure(unittest.TestCase):
    def test_output_contains_metadata_and_all_levels(self):
        test_log("Start test_output_contains_metadata_and_all_levels using helper")

        log_content = [
            "Critical issue",
            "error occurred",
            "failed login",
            "Debug line",
            "Info update",
            "Warning issued",
            "No match here"
        ]

        exit_code, output_json, used_log_path, _ = run_main_for_test(
            log_content_lines=log_content
        )

        if exit_code != 0:
            failThis("main.main() returned a non-zero exit code")

        if output_json is None:
            failThis("Output JSON was not created or was unparsable by helper.")
            return
        expected_levels_in_json = ["CRITICAL", "ERROR", "FAILED", "DEBUG", "INFO", "WARNING", "UNKNOWN", "metadata"]

        test_log(f"Verifying that all expected keys are present in the output: {expected_levels_in_json}")

        actual_keys = set(output_json.keys())

        for level in expected_levels_in_json:
            if level not in actual_keys:
                failThis(f"Key '{level}' not found in output JSON. Found keys: {list(actual_keys)}")

        metadata = output_json.get("metadata", {})
        if metadata.get("total_lines_processed") != len(log_content):
            failThis(
                f"Expected 'total_lines_processed' to be {len(log_content)}, got {metadata.get('total_lines_processed')}.")

        if metadata.get("log_file_path") != used_log_path:
            failThis(f"Expected log_file_path in metadata to be {used_log_path}, got {metadata.get('log_file_path')}")

        test_log("All expected keys and metadata found in the output file.")