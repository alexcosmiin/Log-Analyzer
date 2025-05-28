import subprocess
import os
import unittest
from tests.common_functions import test_log, failThis

class TestLogFileVisibility(unittest.TestCase):
    def test_log_file_is_visible_in_docker(self):
        test_log("🔎 Start test_log_file_is_visible_in_docker Integration Test")
        test_log("📂 Get absolute path to log.txt on the host")
        host_log_path = os.path.abspath("logs/log.txt")
        assert os.path.exists(host_log_path), "'log.txt' does not exist on the host."

        test_log("🐳 Run minimal container to read and print log.txt content")
        docker_command = [
            "docker", "run", "--rm",
            "-v", f"{host_log_path}:/app/log.txt",
            "python:3.10-slim",
            "bash", "-c", "cat /app/log.txt"
        ]

        result = subprocess.run(
            docker_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            failThis(f"Docker command failed: {result.stderr}")

        test_log("🔍 Check expected log entries inside container output")
        if "Login failed" not in result.stdout:
            failThis("Expected 'Login failed' log entry not found in container output.")
        if "Payment succeeded" not in result.stdout:
            failThis("Expected 'Payment succeeded' log entry not found in container output.")
        if "Something else failed" not in result.stdout:
            failThis("Expected 'Something else failed' log entry not found in container output.")
