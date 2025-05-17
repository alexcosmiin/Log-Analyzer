from datetime import timedelta

from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama


class ConsoleReporter:
    def __init__(self, verbosity=1):
        self.verbosity = verbosity
        self.colors = {
            'passed': Fore.GREEN,
            'failed': Fore.RED,
            'error': Fore.YELLOW,
            'info': Fore.CYAN
        }

    def print_report(self, results):
        self._print_header(results)
        self._print_summary(results)

        if self.verbosity >= 1:
            self._print_failed_tests(results)

        if self.verbosity >= 2:
            self._print_all_tests(results)

    def _print_header(self, results):
        duration = timedelta(seconds=results['duration'])
        print(f"\n{Style.BRIGHT}{Fore.BLUE}=== TEST EXECUTION REPORT ===")
        print(f"{Fore.WHITE}Execution time: {duration}{Style.RESET_ALL}\n")

    def _print_summary(self, results):
        total = results['total']
        passed = results['passed']
        failed = results.get('failed', 0)
        errors = results.get('errors', 0)

        pass_percent = (passed / total) * 100 if total > 0 else 0

        print(f"{Style.BRIGHT}{Fore.BLUE}SUMMARY:{Style.RESET_ALL}")
        print(f"  {Style.BRIGHT}Total:{Style.RESET_ALL}    {total}")
        print(f"  {self.colors['passed']}Passed:{Style.RESET_ALL}   {passed} ({pass_percent:.1f}%)")

        if failed > 0:
            print(f"  {self.colors['failed']}Failed:{Style.RESET_ALL}   {failed}")

        if errors > 0:
            print(f"  {self.colors['error']}Errors:{Style.RESET_ALL}  {errors}")

    def _print_test_card(self, test):
        status = test['status'].lower()
        color = self.colors.get(status, Fore.WHITE)

        print(f"\n  {color}{Style.BRIGHT}{status.upper()}{Style.RESET_ALL} {test['name']}")
        print(f"  {Fore.WHITE}Duration: {test['duration']:.3f}s{Style.RESET_ALL}")

        for step in test['steps']:
            step_color = self.colors.get(step['status'], Fore.WHITE)
            print(f"  {step_color}▶ {step['description']} ({step['duration']:.3f}s){Style.RESET_ALL}")
            if step.get('error'):
                print(f"    {Fore.RED}ERROR: {step['error']}{Style.RESET_ALL}")

    def _print_failed_tests(self, results):
        if any(t['status'].lower() != 'passed' for t in results['tests']):
            print(f"\n{Style.BRIGHT}{Fore.RED}DETAILED FAILURES:{Style.RESET_ALL}")
            for test in results['tests']:
                if test['status'].lower() != 'passed':
                    self._print_test_card(test)

    def _print_all_tests(self, results):
        print(f"\n{Style.BRIGHT}{Fore.BLUE}ALL TEST RESULTS:{Style.RESET_ALL}")
        for test in results['tests']:
            self._print_test_card(test)