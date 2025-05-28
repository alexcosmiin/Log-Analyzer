import subprocess
import unittest
import os
from tests.common_functions import test_log, failThis

class TestAppRun(unittest.TestCase):
    def test_app_runs_successfully_in_container(self):
        test_log("🚀 Starting test_app_runs_successfully_in_container")

        test_log("Building Docker command to run the application as a module.")
        docker_command = [
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}:/app",
            "log-analyzer",
            "python3", "-m", "src.main"
        ]

        test_log(f"Executing command: {' '.join(docker_command)}")
        result = subprocess.run(
            docker_command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            failThis(f"App failed to run in container. Stderr: {result.stderr}")

        test_log("✅ Application ran successfully in Docker container")