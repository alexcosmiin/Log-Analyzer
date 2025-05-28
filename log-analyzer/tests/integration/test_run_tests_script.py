import subprocess
import unittest
import os
from tests.common_functions import test_log, failThis


class TestRunTestsScript(unittest.TestCase):
    def test_run_tests_py_script_runs(self):
        test_log("▶️ Running run_tests.py script inside Docker container")

        docker_command = [
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}:/app",
            "log-analyzer",
            "python3", "run_tests.py"
        ]

        test_log(f"Executing command: {' '.join(docker_command)}")
        result = subprocess.run(
            docker_command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            failThis(f"run_tests.py script failed. Stderr: {result.stderr}")
        test_log("✅ run_tests.py executed successfully")