import subprocess
import unittest
import tempfile
import pathlib
import os
from tests.common_functions import test_log, failThis

class TestAppRobustness(unittest.TestCase):
    def test_app_handles_bad_log_file_gracefully(self):
        test_log("⚠️ Testing app behavior with a log file that is a directory")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = pathlib.Path(tmpdir)
            corrupted_log_path_on_host = tmp_path / "corrupted_log.txt"
            os.makedirs(corrupted_log_path_on_host)
            test_log(f"📝 Created a directory named 'corrupted_log.txt' at {corrupted_log_path_on_host}")

            log_file_in_container = "/testdata/corrupted_log.txt"
            docker_command = [
                "docker", "run", "--rm",
                "-v", f"{tmp_path}:/testdata",
                "log-analyzer",
                "python3", "-m", "src.main", "--log-file", log_file_in_container
            ]

            test_log(f"🐳 Running container with log path pointing to a directory: {' '.join(docker_command)}")
            result = subprocess.run(docker_command, capture_output=True, text=True)
            stdout_lower = result.stdout.lower()
            expected_message_part1 = "failed to read log file"
            expected_message_part2 = "log file not found"

            if not (expected_message_part1 in stdout_lower or expected_message_part2 in stdout_lower):
                failThis(
                    f"App did not report an expected error message. Stdout: {result.stdout}, Stderr: {result.stderr}")
            test_log("✅ App handled the bad log file (directory) gracefully by reporting an error.")