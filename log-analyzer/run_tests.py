import sys
import threading
import unittest
import argparse
import time
import os
from test_framework.reporting import HTMLReporter
from colorama import Fore, Style, init
from tests.common_functions import test_logs, TestFailure
from datetime import datetime
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
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
    base_discover_dir = os.path.join(SCRIPT_DIR, 'tests')

    start_dir_to_discover = base_discover_dir
    if category:
        start_dir_to_discover = os.path.join(base_discover_dir, category)
    print(f"Discovering tests in: {start_dir_to_discover} (Top level: {SCRIPT_DIR})")
    suite = loader.discover(
        start_dir=start_dir_to_discover,
        pattern='test_*.py',
        top_level_dir=SCRIPT_DIR
    )
    tests = flatten_suite(suite)
    print(f"Number of tests discovered: {len(tests)}")
    return tests


def format_test_name(test):
    test_file = test.__class__.__module__
    test_path = getattr(test, "__test_file__", None)
    if not test_path:
        test_path = os.path.abspath(sys.modules[test.__class__.__module__].__file__)
    category = os.path.basename(os.path.dirname(test_path))
    return f"{category}_tests.{test._testMethodName}"


def print_test_result(test, status, message=""):
    color = Fore.GREEN if status == 'PASSED' else Fore.RED
    symbol = '✓' if status == 'PASSED' else '✗'
    test_name = format_test_name(test)
    print(f"{color}[{symbol}] {test_name}{Style.RESET_ALL}")
    if message:
        for line in message.strip().split('\n'):
            if line.strip():
                print(f"    → {line}")
    print()



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

    print()  # spacing between list and results

    test_results = {
        'execution_time': '0.000s',
        'total': 0,
        'passed': 0,
        'failed': 0,
        'success_rate': 0,
        'tests': []
    }

    failures = []
    errors = []
    start_time = time.time()

    for test in all_tests:
        test_results['total'] += 1
        thread_id = threading.get_ident()

        try:
            test.setUp()
            getattr(test, test._testMethodName)()
            test.tearDown()

            log_output = '\n'.join(test_logs.get(thread_id, []))
            print_test_result(test, 'PASSED', log_output)
            test_results['tests'].append({
                'name': str(test),
                'status': 'PASSED',
                'duration': '0.000s',
                'message': log_output
            })
        except TestFailure as tf:
            log_output = '\n'.join(test_logs.get(thread_id, []))
            full_message = tf.message
            if log_output:
                full_message = f"{log_output}\n{tf.message}" if tf.message else log_output

            # Check if test method is expected failure
            test_method = getattr(test, test._testMethodName)
            if hasattr(test_method, '_expected_failure'):
                # Mark as PASSED with note of expected failure
                full_message = f"EXPECTED FAILURE:\n{full_message}"
                print_test_result(test, 'PASSED', full_message)
                test_results['tests'].append({
                    'name': str(test),
                    'status': 'PASSED',
                    'duration': '0.000s',
                    'message': full_message
                })
            else:
                failures.append((test, tf.message))
                print_test_result(test, 'FAILED', full_message)
                test_results['tests'].append({
                    'name': str(test),
                    'status': 'FAILED',
                    'duration': '0.000s',
                    'message': full_message
                })

        except Exception as e:
            log_output = '\n'.join(test_logs.get(thread_id, []))
            full_message = f"{log_output}\n\n{str(e)}" if log_output else str(e)
            errors.append((test, str(e)))
            print_test_result(test, 'FAILED', full_message)
            test_results['tests'].append({
                'name': str(test),
                'status': 'FAILED',
                'duration': '0.000s',
                'message': full_message
            })

        finally:
            test_logs.pop(thread_id, None)

    duration = time.time() - start_time
    test_results['execution_time'] = f"{duration:.3f}s"
    test_results['passed'] = test_results['total'] - len(failures) - len(errors)
    test_results['failed'] = len(failures) + len(errors)
    test_results['success_rate'] = (test_results['passed'] / test_results['total'] * 100
                                    if test_results['total'] > 0 else 0)

    print(f"\n{Fore.CYAN}=== SUMMARY ==={Style.RESET_ALL}")
    print(f"Total: {test_results['total']}")
    print(f"{Fore.GREEN}Passed: {test_results['passed']}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {len(failures)}{Style.RESET_ALL}")
    print(f"{Fore.RED}Errors: {len(errors)}{Style.RESET_ALL}")
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
