from .function_executor_thread import wrap_function_in_executor_thread
from .timeout_thread import TimeoutThread


def timeout(timeout_seconds: int):
    """
    Wraps the target function in a proxy function that will delegate the execution of the original function to
    a separate thread.

    The separate thread will have the functionality to wait for the function to complete and return its result or
    raise a TimeoutException if the function cannot finish executing within the specified timeout interval.

    :param timeout_seconds: The number of seconds to wait for the given function to complete execution before
        forcing the thread running the function to quit.
    :return: The wrapped function to be invoked in place of the function being decorated.
    """

    def inner(function):
        def wrapper(*args, **kwargs):
            executor_thread = wrap_function_in_executor_thread(lambda: function(*args, **kwargs))
            timeout_thread = TimeoutThread(timeout_seconds, executor_thread)
            timeout_thread.start()
            timeout_thread.join()
            if not timeout_thread.did_executor_thread_complete():
                raise timeout_thread.get_exception()
            else:
                result = executor_thread.get_execution_result()
                exception = result.get_exception()
                if exception is not None:
                    raise exception
                return result.get_return_value()
        return wrapper
    return inner
