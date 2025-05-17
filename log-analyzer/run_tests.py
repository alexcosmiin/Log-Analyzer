import threading
import unittest
import argparse
import time
import os
from test_framework.reporting import HTMLReporter
from colorama import Fore, Style, init
from tests.common_functions import test_logs
from datetime import datetime

init(autoreset=True)


def flatten_suite(suite):
    tests = []
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            tests.extend(flatten_suite(test))
        else:
            tests.append(test)
    return tests


def discover_tests(category=None):
    loader = unittest.TestLoader()
    start_dir = os.path.join('tests', category) if category else 'tests'
    suite = loader.discover(start_dir=start_dir, pattern='test_*.py')
    return flatten_suite(suite)


def print_test_result(test_name, status, message=""):
    color = Fore.GREEN if status == 'PASSED' else Fore.RED
    symbol = '✓' if status == 'PASSED' else '✗'
    print(f"{color}[{symbol}] {test_name}{Style.RESET_ALL}")
    if message and status != 'PASSED':
        print(f"{Fore.YELLOW}Details:{Style.RESET_ALL}")
        print(message)


def format_test_name(test):
    return f"{test.__class__.__module__}.{test.__class__.__name__}.{test._testMethodName}"


def run_tests(filter_str=None, category=None):
    all_tests = discover_tests(category)

    if filter_str:
        all_tests = [
            test for test in all_tests
            if filter_str.lower() in format_test_name(test).lower()
        ]

    if not all_tests:
        print(f"{Fore.YELLOW}No tests found matching your criteria.{Style.RESET_ALL}")
        return {
            'execution_time': '0.000s',
            'total': 0,
            'passed': 0,
            'failed': 0,
            'success_rate': 0,
            'tests': []
        }

    print(f"\n{Fore.CYAN}=== RUNNING {len(all_tests)} TEST(S) ==={Style.RESET_ALL}\n")
    for test in all_tests:
        print(f"[ ] {format_test_name(test)}")

    start_time = time.time()
    result = unittest.TextTestRunner(verbosity=0).run(unittest.TestSuite(all_tests))

    test_results = {
        'execution_time': f"{time.time() - start_time:.3f}s",
        'total': result.testsRun,
        'passed': result.testsRun - len(result.failures) - len(result.errors),
        'failed': len(result.failures) + len(result.errors),
        'success_rate': (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
        if result.testsRun > 0 else 0,
        'tests': []
    }

    failed_or_errored = [f[0] for f in result.failures + result.errors]
    passed_tests = [test for test in all_tests if test not in failed_or_errored]

    for test in passed_tests:
        name = str(test)
        thread_id = threading.get_ident()
        log_output = '\n'.join(test_logs.get(thread_id, []))
        test_results['tests'].append({
            'name': name,
            'status': 'PASSED',
            'duration': '0.000s',
            'message': log_output
        })
        print_test_result(name, 'PASSED')
        test_logs.pop(threading.get_ident(), None)

    for test, traceback in result.failures + result.errors:
        name = str(test)
        thread_id = threading.get_ident()
        log_output = '\n'.join(test_logs.get(thread_id, []))
        full_message = f"{log_output}\n\n{traceback}" if log_output else traceback
        test_results['tests'].append({
            'name': name,
            'status': 'FAILED',
            'duration': '0.000s',
            'message': full_message
        })
        print_test_result(name, 'FAILED', full_message)
        test_logs.pop(threading.get_ident(), None)

    print(f"\n{Fore.CYAN}=== SUMMARY ==={Style.RESET_ALL}")
    print(f"Total: {test_results['total']}")
    print(f"{Fore.GREEN}Passed: {test_results['passed']}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {len(result.failures)}{Style.RESET_ALL}")
    print(f"{Fore.RED}Errors: {len(result.errors)}{Style.RESET_ALL}")
    print(f"Success rate: {test_results['success_rate']:.1f}%")
    print(f"Duration: {test_results['execution_time']}")

    return test_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run selected tests")
    parser.add_argument('--filter', help="Run tests matching name (substring match)", default=None)
    parser.add_argument('--category', help="Run tests only from a specific category directory", default=None)
    args = parser.parse_args()

    results = run_tests(filter_str=args.filter, category=args.category)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"reports/test_report_{timestamp}.html"
    html_reporter = HTMLReporter()
    html_reporter.generate(results, output_file)
    print(f"HTML report saved to: {output_file}")
