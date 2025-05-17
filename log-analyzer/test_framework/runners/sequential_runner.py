import inspect
import time

from .base_runner import BaseRunner
from ..core.test_case import TestCase


class SequentialTestRunner(BaseRunner):
    """Runs tests sequentially in a single thread"""

    def _run_test_class(self, test_class: type):
        test_instance = test_class()

        # Get all test methods
        test_methods = [
            m for m in inspect.getmembers(test_class, inspect.isfunction)
            if m[0].startswith('test_')
        ]

        for name, method in test_methods:
            self._run_test_method(test_instance, name, method)

    def _run_test_method(self, instance: TestCase, name: str, method):
        start_time = time.time()
        status = 'passed'

        try:
            # Run setup if exists
            if hasattr(instance, 'setup'):
                instance.setup()

            # Run the test
            method(instance)

        except AssertionError:
            status = 'failed'
        except Exception:
            status = 'error'
        finally:
            # Run teardown if exists
            if hasattr(instance, 'teardown'):
                instance.teardown()

            duration = time.time() - start_time
            self._record_test_result(
                f"{instance.__class__.__name__}.{name}",
                status,
                duration,
                instance.steps
            )