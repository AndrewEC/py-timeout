from threading import Thread
from time import sleep
import math
import ctypes

from .function_executor import FunctionExecutorThread
from .atomic_reference import AtomicReference
from .timeout_exception import TimeoutException


class TimeoutThread(Thread):

    """
    A thread for monitoring the execution of a FunctionExecutorThread in which said FunctionExecutorThread will
    be responsible for the execution of an underlying function.

    When used this thread allows the FunctionExecutorThread to be executed and monitored with the purpose of
    allowing the thread to complete if it does so within the specified execution time or forcefully terminating
    the thread and raising an exception when the execution of the monitored thread exceeds the configured value.
    """

    _WAIT_TIME = 0.25

    def __init__(self, execution_timeout: int, thread_to_monitor: FunctionExecutorThread):
        super().__init__()
        self._execution_exception = AtomicReference[Exception]()
        self._execution_timeout = execution_timeout
        self._wait_iterations = math.floor(int(execution_timeout / TimeoutThread._WAIT_TIME))
        self._thread_to_monitor = thread_to_monitor

    def run(self) -> None:
        self._thread_to_monitor.start()

        # Wait for the function executor thread to complete naturally.
        for _ in range(self._wait_iterations):
            if not self._thread_to_monitor.is_running():
                break
            sleep(TimeoutThread._WAIT_TIME)

        # If is_running is true then the function executor thread is still running after the timeout interval elapsed.
        if self._thread_to_monitor.is_running():
            try:
                self._force_quit_executor_thread()
                self._execution_exception.set_value(TimeoutException(f'The function did not complete within in the allotted [{self._execution_timeout}] seconds.'))
            except Exception as e:
                self._execution_exception.set_value(e)
        else:
            # The function executor thread should have finished naturally if we reached this point.
            self._thread_to_monitor.join()

    def _force_quit_executor_thread(self):
        """
        Adapted from the answer: https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
        """

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._thread_to_monitor.ident), exc)
        if res == 0:
            raise ValueError("Timeout thread exceeded timeout limit. Could not stop timeout thread. Non-existent thread id.")
        elif res > 1:
            # If it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self._thread_to_monitor.ident, None)
            raise SystemError("Timeout thread exceeded timeout limit. An issue occurred while stopping timeout thread. PyThreadState_SetAsyncExc failed.")

    def did_executor_thread_complete(self):
        """
        Indicates if the executor thread currently being monitored completed execution within the specified time
        period or not.

        :return: True if the execution completed in a timely manner, otherwise false.
        """
        return self._execution_exception.get_value() is None

    def get_exception(self) -> Exception | None:
        """
        Returns a TimeoutException if the thread being monitored failed to completed execution in the time specified.

        If the monitored thread did complete successfully then this will return None.

        :return: None if the monitored thread completed execution in a timely manner, otherwise a TimeoutException
        """
        return self._execution_exception.get_value()
