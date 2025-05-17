from datetime import datetime
from typing import List, Dict, Any


class BaseRunner:
    """Base class for all test runners"""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'duration': 0.0,
            'tests': []
        }

    def run(self, test_classes: List[type]) -> Dict[str, Any]:
        """Execute tests and return results"""
        self.start_time = datetime.now()

        for test_class in test_classes:
            self._run_test_class(test_class)

        self.end_time = datetime.now()
        self.results['duration'] = (self.end_time - self.start_time).total_seconds()

        return self.results

    def _run_test_class(self, test_class: type):
        """Override with specific test execution logic"""
        raise NotImplementedError

    def _record_test_result(self, test_name: str, status: str,
                            duration: float, steps: List[Dict]):
        """Record individual test results"""
        self.results['total'] += 1

        if status == 'passed':
            self.results['passed'] += 1
        else:
            self.results['failed'] += 1

        self.results['tests'].append({
            'name': test_name,
            'status': status,
            'duration': duration,
            'steps': steps
        })