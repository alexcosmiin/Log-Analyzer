import unittest
from contextlib import contextmanager
from datetime import datetime


class TestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()  # Crucial for unittest integration
        self.steps = []

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.steps = []

    def add_step(self, description):
        """Manual step creation (returns context manager)"""
        return self._step_context(description)

    def step_success(self, message=""):
        """For backward compatibility"""
        pass

    def step_fail(self, message=""):
        """For backward compatibility"""
        pass

    @contextmanager
    def _step_context(self, description):
        step = {
            'description': description,
            'status': 'running',
            'start_time': datetime.now(),
            'duration': None,
            'error': None
        }
        self.steps.append(step)

        try:
            yield
            step['status'] = 'passed'
        except Exception as e:
            step['status'] = 'failed'
            step['error'] = str(e)
            raise
        finally:
            step['duration'] = (datetime.now() - step['start_time']).total_seconds()