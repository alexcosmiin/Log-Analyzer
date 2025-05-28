import subprocess
import unittest
import os
from tests.common_functions import test_log, failThis

class TestCLIParameters(unittest.TestCase):
    def test_cli_parameters_are_respected(self):
        test_log("⚙️ Testing CLI parameters handling")

        docker_command = [
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}:/app",
            "log-analyzer",
            "python3", "-m", "src.main", "--verbose"
        ]

        test_log(f"Executing command: {' '.join(docker_command)}")
        result = subprocess.run(
            docker_command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            failThis(f"App failed to run with CLI parameter. Stderr: {result.stderr}")

        test_log("🔍 Checking for verbose mode output in stdout.")
        if "verbose mode enabled" not in result.stdout.lower():
            failThis("Verbose mode output expected but not found in stdout.")

        test_log("✅ CLI parameters handled correctly.")