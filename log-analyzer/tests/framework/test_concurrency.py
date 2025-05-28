import unittest
import threading
from tests.common_functions import test_log, failThis

class TestConcurrency(unittest.TestCase):

    def test_thread_safe_logs(self):
        test_log("Testing concurrent logging from multiple threads")

        messages = []
        def worker(i):
            test_log(f"Thread {i} logging")
            messages.append(f"Thread {i} done")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if len(messages) != 5:
            failThis(f"Expected 5 log messages but got {len(messages)}")
        test_log("Concurrent logging test completed successfully")
