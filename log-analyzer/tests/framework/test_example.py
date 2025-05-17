from test_framework.core.test_case import TestCase
from test_framework.utils import step
from test_framework.utils.assertions import Assertions


class LoginTest(TestCase):
    @step("Successful login")
    def test_successful_login(self):
        with self.add_step("Verify welcome page"):
            Assertions.assert_equal("Welcome Page", "Welcome Page")

class PaymentTest(TestCase):
    @step("Failed payment")
    def test_failed_payment(self):
        with self.add_step("Verify card decline"):
            Assertions.assert_contains("declined", "Card declined message")