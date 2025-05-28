import unittest
import os
from tests.common_functions import test_log, failThis

class TestResourceCleanup(unittest.TestCase):

    def test_cleanup(self):
        test_log("Testing resource cleanup after tests")

        temp_file = "temp_test_file.txt"
        try:
            with open(temp_file, "w") as f:
                f.write("temporary content")

            if not os.path.exists(temp_file):
                failThis("Temporary file was not created")

            # Simulate test cleanup:
            os.remove(temp_file)

            if os.path.exists(temp_file):
                failThis("Temporary file was not removed in cleanup")
        except Exception as e:
            failThis(f"Resource cleanup test failed: {e}")
