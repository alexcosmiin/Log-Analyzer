import subprocess
from tests.common_functions import *
import unittest

class SmokeMainRuns(unittest.TestCase):
    def test_main_runs_successfully(self):
        test_log("Smoke Test: Running main.py inside Docker to check basic execution.")

        result = subprocess.run(
            ["docker", "run", "--rm", "-v", "$(pwd)/logs:/app/logs", "-v", "$(pwd)/output:/app/output", "log-analyzer"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        if result.returncode != 0:
            failThis(f"main.py failed to run inside Docker. Error: {result.stderr}")

        if "Log classification complete" not in result.stdout:
            failThis("Expected success message not found in output.")
