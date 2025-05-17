import os
import unittest
from tests.common_functions import test_log

class SmokeTest(unittest.TestCase):
    def test_log_file_exists(self):
        test_log("Check if log file exists...")
        self.assertTrue(os.path.exists("logs/log.txt"), "File logs/log.txt doesn't exists.")
        test_log("File logs/log.txt doesn't exists, test succeded.")
