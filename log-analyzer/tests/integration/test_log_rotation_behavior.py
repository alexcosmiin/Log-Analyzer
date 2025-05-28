import subprocess
import os
import unittest

from tests.common_functions import test_log, failThis

class TestLogRotationBehavior(unittest.TestCase):
    def test_log_rotation_triggers_output_regeneration(self):
        test_log("🔄 Testing if log rotation triggers output regeneration")

        log_path = os.path.abspath("logs/log.txt")
        test_log("✍️ Appending log rotation test entry to log file")
        with open(log_path, "a") as f:
            f.write("Log rotation test entry\n")

        test_log("🐳 Running container to process log after rotation")
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", "log-analyzer"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            failThis(f"Container failed to run: {result.stderr}")

        import time
        output_path = os.path.abspath("output/output.json")
        mtime = os.path.getmtime(output_path)
        now = time.time()
        if now - mtime > 120:
            failThis("Output file not regenerated after log rotation")

        test_log("✅ Log rotation triggers output regeneration")
