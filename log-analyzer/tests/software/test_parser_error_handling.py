import unittest
import tempfile
import pathlib

from src.parser import read_log_file
from tests.common_functions import failThis, test_log


class ParserErrorHandling(unittest.TestCase):
    def test_read_log_file_not_found(self):
        test_log("Start test_read_log_file_not_found")
        missing_file = "tests/software/nonexistent_file.log"
        test_log(f"Attempting to read a non-existent file: {missing_file}")

        try:
            read_log_file(missing_file)
            failThis(f"Expected FileNotFoundError for {missing_file} but it was not raised.")
        except FileNotFoundError:
            test_log("Successfully caught FileNotFoundError as expected.")
        except Exception as e:
            failThis(f"Caught an unexpected exception type: {type(e).__name__} with message: {e}")

    def test_read_log_file_bad_encoding(self):
        test_log("Start test_read_log_file_bad_encoding")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = pathlib.Path(tmpdir)
            test_log(f"Created temporary directory: {tmp_path}")

            bad_file = tmp_path / "bad_encoding.log"
            invalid_bytes = b'\xff\xfe\xfa\xfb\xfc'
            bad_file.write_bytes(invalid_bytes)
            test_log(f"Created a file with invalid UTF-8 bytes at: {bad_file}")

            test_log("Reading the file, expecting it to be successfully decoded with latin-1.")
            lines = read_log_file(str(bad_file))

            test_log("Verifying the content returned by the latin-1 fallback.")
            expected_content = invalid_bytes.decode('latin-1')

            if not lines:
                failThis("Function returned an empty list instead of decoded content.")

            if lines[0].strip() != expected_content:
                failThis(f"Expected content '{expected_content}' but got '{lines[0].strip()}'")

            test_log("Content was successfully decoded and verified.")