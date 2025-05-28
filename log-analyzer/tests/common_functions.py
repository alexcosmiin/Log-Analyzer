import os
import subprocess
import threading
import json
import tempfile
import pathlib
from unittest import mock
import sys
import src.main as main_module

test_logs = {}
test_fail_reasons = {}


class TestFailure(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def test_log(message):
    thread_id = threading.get_ident()
    if thread_id not in test_logs:
        test_logs[thread_id] = []
    test_logs[thread_id].append(message)

def failThis(reason: str):
    thread_id = threading.get_ident()
    test_fail_reasons[thread_id] = reason
    raise TestFailure(reason)

def create_test_log(lines=None):
    os.makedirs("logs", exist_ok=True)
    with open("logs/log.txt", "w") as f:
        f.writelines((line + "\n") for line in (lines or [
            "Login failed for user John",
            "Payment succeeded",
            "Something else failed"
        ]))

def run_analysis_script():
    return subprocess.run(["bash", "start_script.sh"], capture_output=True, text=True)

def load_output_json():
    with open("output/output.json", "r") as f:
        return json.load(f)

def file_exists(path):
    return os.path.exists(path)

def expected_failure(func):
    func._expected_failure = True
    return func

def run_main_for_test(log_content_lines=None, cli_extra_args=None):
    if log_content_lines is None:
        log_content_lines = []
    if cli_extra_args is None:
        cli_extra_args = []

    parsed_json = None
    exit_code = -1

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir_path = pathlib.Path(tmpdir)

        log_file_path = temp_dir_path / "temp_test.log"
        output_file_path = temp_dir_path / "temp_output.json"

        log_file_path.write_text("\n".join(log_content_lines))
        test_log(f"Helper: Created temp log file at {log_file_path} with {len(log_content_lines)} lines.")
        test_log(f"Helper: Output will be at {output_file_path}.")

        mock_argv = [
                        "src/main.py",
                        "--log-file", str(log_file_path),
                        "--output-file", str(output_file_path)
                    ] + cli_extra_args

        with mock.patch.object(sys, 'argv', mock_argv):
            test_log(f"Helper: Executing main_module.main() with sys.argv: {mock_argv}")
            exit_code = main_module.main()

        if output_file_path.exists():
            try:
                parsed_json = json.loads(output_file_path.read_text())
                test_log("Helper: Successfully loaded output JSON from temp file.")
            except json.JSONDecodeError as e:
                test_log(f"Helper: Failed to parse output JSON: {e}. Content: {output_file_path.read_text()[:200]}")
        else:
            test_log("Helper: Output JSON file was not created.")

    return exit_code, parsed_json, str(log_file_path), str(output_file_path)