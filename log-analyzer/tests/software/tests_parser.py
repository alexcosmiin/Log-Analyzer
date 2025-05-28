import os
from src.parser import read_log_file
from tests.common_functions import failThis, test_log
import unittest

class TestsParser(unittest.TestCase):
    def test_read_log_file_success(self):
        test_log("Start test_read_log_file_success")
        test_file = "tests/software/test_log.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Info: test line 1\nError: test line 2\n")
        try:
            lines = read_log_file(test_file)
            assert len(lines) == 2
            assert "Info: test line 1\n" in lines
        except Exception as e:
            failThis(f"read_log_file failed unexpectedly: {e}")
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_read_log_file_not_found(self):
        test_log("Start test_read_log_file_not_found")
        try:
            read_log_file("non_existent_file.log")
            failThis("read_log_file should raise FileNotFoundError for missing file")
        except FileNotFoundError:
            test_log("Caught expected FileNotFoundError")
        except Exception as e:
            failThis(f"read_log_file raised unexpected exception: {e}")
