class TestSuite:
    def __init__(self, name=""):
        self.name = name
        self.test_cases = []
        self.setup_hooks = []
        self.teardown_hooks = []

    def add_test_case(self, test_case):
        self.test_cases.append(test_case)

    def add_setup(self, hook):
        self.setup_hooks.append(hook)

    def add_teardown(self, hook):
        self.teardown_hooks.append(hook)

    def run(self):
        results = []
        for hook in self.setup_hooks:
            hook()

        for test_case in self.test_cases:
            results.append(test_case.run())

        for hook in self.teardown_hooks:
            hook()

        return results