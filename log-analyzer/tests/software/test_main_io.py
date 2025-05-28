import unittest
from tests.common_functions import test_log, failThis, run_main_for_test


class MainIO(unittest.TestCase):
    def test_main_output_file_creation(self):
        test_log("Start test_main_output_file_creation using helper")

        log_content = ["Critical failure", "Info message", "Error detected"]

        exit_code, output_json, used_log_path, used_output_path = run_main_for_test(
            log_content_lines=log_content
        )

        if exit_code != 0:
            failThis(f"main.main() returned non-zero exit code {exit_code}")

        if output_json is None:
            failThis("Output JSON was not created or was unparsable by helper.")
            return

        test_log("Verifying output file was effectively created (by checking parsed JSON).")

        test_log("Verifying JSON content: CRITICAL count and metadata.")
        critical_data = output_json.get("CRITICAL", {})
        if critical_data.get("count") != 1:
            failThis(
                f"CRITICAL log count incorrect. Expected 1, got {critical_data.get('count')}. Data: {critical_data}")

        metadata = output_json.get("metadata", {})
        if metadata.get("total_lines_processed") != 3:
            failThis(
                f"Metadata total_lines_processed incorrect. Expected 3, got {metadata.get('total_lines_processed')}.")

        if metadata.get("log_file_path") != used_log_path:
            failThis(f"Expected log_file_path in metadata to be {used_log_path}, got {metadata.get('log_file_path')}")

        test_log("Test finished successfully.")