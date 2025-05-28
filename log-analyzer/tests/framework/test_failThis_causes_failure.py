import unittest
from tests.common_functions import test_log, failThis

class TestFailThisCausesFailure(unittest.TestCase):

    def test_failThis_behavior(self):
        test_log("Testing failThis() triggers failure")
        try:
            failThis("Intentional failure")
            failThis("failThis() did NOT stop execution")
        except Exception:
            # Expected to raise/fail
            pass
        else:
            failThis("failThis() did NOT raise exception as expected")
