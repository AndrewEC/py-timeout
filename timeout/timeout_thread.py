from threading import Thread
from time import sleep
import math
import ctypes

from .function_executor import FunctionExecutorThread
from .container import ValueContainer


class TimeoutThread(Thread):

    _WAIT_TIME = 0.25

    def __init__(self, execution_timeout: int, thread_to_execute_under_timeout: FunctionExecutorThread):
        super().__init__()
        self.execution_exception = ValueContainer[Exception]()
        self._execution_timeout = execution_timeout
        self._wait_iterations = math.floor(int(execution_timeout / TimeoutThread._WAIT_TIME))
        self._thread_to_execute_under_timeout = thread_to_execute_under_timeout

    def run(self) -> None:
        self._thread_to_execute_under_timeout.start()

        # Wait for the function executor thread to complete naturally.
        for _ in range(self._wait_iterations):
            if not self._thread_to_execute_under_timeout.is_running():
                break
            sleep(TimeoutThread._WAIT_TIME)

        # If is_running is true then the function executor thread is still running after the timeout interval elapsed.
        if self._thread_to_execute_under_timeout.is_running():
            try:
                self._force_quit_executor_thread()
                self.execution_exception.set_value(SystemError(f'The timeout thread did not complete in the allotted [{self._execution_timeout}] seconds.'))
            except Exception as e:
                self.execution_exception.set_value(e)
        else:
            # The function executor thread should have finished naturally if we reached this point.
            self._thread_to_execute_under_timeout.join()

    def _force_quit_executor_thread(self):
        """
        Adapted from the answer: https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
        """

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._thread_to_execute_under_timeout.ident), exc)
        if res == 0:
            raise ValueError("Timeout thread exceeded timeout limit. Could not stop timeout thread. Non-existent thread id.")
        elif res > 1:
            # If it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self._thread_to_execute_under_timeout.ident, None)
            raise SystemError("Timeout thread exceeded timeout limit. An issue occurred while stopping timeout thread. PyThreadState_SetAsyncExc failed.")

    def did_executor_thread_complete(self):
        return self.get_exception() is None

    def get_exception(self) -> Exception | None:
        execution_exception = self.execution_exception.get_value()
        return execution_exception if execution_exception is not None else self._thread_to_execute_under_timeout.get_exception()
