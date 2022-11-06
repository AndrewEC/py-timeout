import unittest

from ..lib.decorator import timeout
from ..lib.timeout_exception import TimeoutException


class TimeoutTests(unittest.TestCase):

    FUNCTION_RESULT = 'function_result'

    def test_function_that_will_timeout(self):
        with self.assertRaises(TimeoutException):
            timeout(3)(function_that_will_timeout)()

    def test_function_that_will_return_result(self):
        result = timeout(3)(lambda: TimeoutTests.FUNCTION_RESULT)()
        self.assertEqual(TimeoutTests.FUNCTION_RESULT, result)

    def test_function_that_will_throw_exception(self):
        with self.assertRaises(ValueError) as context:
            timeout(3)(function_that_will_throw_exception)()
        self.assertEqual(TimeoutTests.FUNCTION_RESULT, str(context.exception))


def function_that_will_timeout():
    while True:
        pass


def function_that_will_throw_exception():
    raise ValueError(TimeoutTests.FUNCTION_RESULT)

