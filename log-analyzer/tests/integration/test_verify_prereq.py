from test_framework.core.test_case import TestCase
from test_framework.utils import step
from test_framework.utils.assertions import Assertions
from tests.common_functions import (
    create_test_log,
    run_analysis_script,
    load_output_json,
    file_exists
)

class LogAnalyzerIntegrationTest(TestCase):

    @step("Verify log analyzer parses 'failed' lines from logs and generates output")
    def test_log_analysis_output(self):
        with self.add_step("Generate log file"):
            create_test_log([
                "Login failed for user John",
                "Payment succeeded",
                "Something else failed"
            ])

        with self.add_step("Run analyzer inside Docker"):
            result = run_analysis_script()
            Assertions.assert_true(result.returncode == 0, "Script should run successfully")
            print("Docker script output:\n", result.stdout)

        with self.add_step("Check if output.json exists"):
            Assertions.assert_true(file_exists("output/output.json"), "Output file should exist")

        with self.add_step("Validate parsed output content"):
            data = load_output_json()
            failed_lines = data.get("failed_entries", [])
            Assertions.assert_equal(len(failed_lines), 2, "Should detect exactly 2 failed lines")
            Assertions.assert_contains("Login failed", failed_lines[0])
