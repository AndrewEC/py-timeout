import unittest

from ..lib.decorator import timeout
from ..lib.timeout_exception import TimeoutException


class TimeoutTests(unittest.TestCase):

    FUNCTION_RESULT = 'function_result'

    def test_function_that_will_timeout(self):
        with self.assertRaises(TimeoutException):
            function_that_will_timeout()

    def test_function_that_will_return_result(self):
        result = function_that_will_return_result()
        self.assertEqual(TimeoutTests.FUNCTION_RESULT, result)

    def test_function_that_will_throw_exception(self):
        with self.assertRaises(ValueError) as context:
            function_that_will_throw_exception()
        self.assertEqual(TimeoutTests.FUNCTION_RESULT, str(context.exception))


@timeout(3)
def function_that_will_timeout():
    while True:
        pass


@timeout(3)
def function_that_will_return_result() -> str:
    return TimeoutTests.FUNCTION_RESULT


@timeout(3)
def function_that_will_throw_exception():
    raise ValueError(TimeoutTests.FUNCTION_RESULT)

