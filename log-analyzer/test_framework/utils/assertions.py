class Assertions:
    """Fixed assertion methods with correct names"""

    @staticmethod
    def assert_equal(actual, expected, message=""):
        assert actual == expected, f"{message} Expected {expected}, got {actual}"

    @staticmethod
    def assert_contains(item, container, message=""):
        assert item in container, f"{message} {item} not found in {container}"

    @staticmethod
    def assert_true(condition, message=""):
        assert condition, message

    @staticmethod
    def assert_false(condition, message=""):
        assert not condition, message