import unittest
from tests.common_functions import test_log, failThis, run_main_for_test


class MainOnlyUnknownMessagesAreClassified(unittest.TestCase):
    def test_only_unknown_messages_are_classified(self):
        test_log("Start test_only_unknown_messages_are_classified using helper")

        log_content = [
            "no match here",
            "this will be unknown",
            "42",
            "..."
        ]

        exit_code, output_json, used_log_path, _ = run_main_for_test(
            log_content_lines=log_content
        )

        if exit_code != 0:
            failThis(f"main.main() returned non-zero exit code {exit_code}")

        if output_json is None:
            failThis("Output JSON was not created or was unparsable by helper.")
            return

        test_log("Verifying output contains only 'UNKNOWN' and 'metadata' keys.")
        expected_keys = {"UNKNOWN", "metadata"}
        actual_keys = set(output_json.keys())

        if actual_keys != expected_keys:
            failThis(f"Expected only 'UNKNOWN' and 'metadata' keys, but found {list(actual_keys)}")

        test_log("Verifying the count of UNKNOWN entries.")
        unknown_data = output_json.get("UNKNOWN", {})
        if unknown_data.get("count") != 4:
            failThis(f"Expected 4 UNKNOWN entries, but found {unknown_data.get('count')}")

        metadata = output_json.get("metadata", {})
        if metadata.get("total_lines_processed") != len(log_content):
            failThis(
                f"Expected 'total_lines_processed' to be {len(log_content)}, got {metadata.get('total_lines_processed')}.")
        if metadata.get("log_file_path") != used_log_path:
            failThis(f"Expected log_file_path in metadata to be {used_log_path}, got {metadata.get('log_file_path')}")

        test_log("JSON structure and UNKNOWN count are correct.")