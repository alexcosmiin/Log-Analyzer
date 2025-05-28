import unittest
import contextlib
from test_framework.utils.assertions import Assertions
from tests.common_functions import *


class LogAnalyzerIntegrationTest(unittest.TestCase):

    @contextlib.contextmanager
    def add_step(self, description: str):
        test_log(f"--- STEP: {description} --- START ---")
        try:
            yield
        except TestFailure:
            test_log(f"--- STEP: {description} --- FAILED (failThis called) ---")
            raise
        except Exception as e:
            test_log(f"--- STEP: {description} --- ERRORED: {type(e).__name__}: {e} ---")
            raise
        else:
            test_log(f"--- STEP: {description} --- END ---")

    def test_log_analysis_output(self):
        with self.add_step("Generate log file with specific entries"):
            create_test_log([
                "Login failed for user John",
                "Payment succeeded",
                "Something else failed"
            ])

        with self.add_step("Run analyzer script inside Docker container"):
            result = run_analysis_script()
            Assertions.assert_true(result.returncode == 0, f"Script should run successfully. Stderr: {result.stderr}")
            test_log(f"Docker script stdout:\n{result.stdout}")
            if result.stderr:
                test_log(f"Docker script stderr:\n{result.stderr}")

        with self.add_step("Check if output.json was created"):
            Assertions.assert_true(file_exists("output/output.json"), "output/output.json file should exist")

        with self.add_step("Validate parsed output.json content for failed entries"):
            data = load_output_json()

            failed_lines = data.get("FAILED", {}).get("messages", [])

            Assertions.assert_equal(len(failed_lines), 2,
                                    f"Should detect exactly 2 failed lines. Found: {len(failed_lines)}. Lines: {failed_lines}")

            if len(failed_lines) > 0:
                Assertions.assert_contains("Login failed for user John", failed_lines[0],
                                           "The first failed line should contain 'Login failed for user John'")
            else:
                failThis("No failed lines found, but expected 'Login failed for user John' as the first.")