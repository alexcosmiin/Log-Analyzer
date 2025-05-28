import unittest
from tests.common_functions import test_log, failThis

class TestSetupTeardownHooks(unittest.TestCase):

    def test_setup_teardown(self):
        test_log("Testing setup and teardown hooks")

        self.setup_done = False
        self.teardown_done = False

        def setup():
            self.setup_done = True
            test_log("Setup executed")

        def teardown():
            self.teardown_done = True
            test_log("Teardown executed")

        try:
            setup()
            # simulate test body here
            teardown()
        except Exception as e:
            failThis(f"Setup/teardown raised exception: {e}")

        if not (self.setup_done and self.teardown_done):
            failThis("Setup or teardown did not run")
