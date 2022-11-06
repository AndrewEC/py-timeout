from .function_executor_thread import wrap_function_in_executor_thread
from .timeout_thread import TimeoutThread


def timeout(timeout_seconds: int):
    def inner(function):
        def wrapper(*args, **kwargs):
            executor_thread = wrap_function_in_executor_thread(lambda: function(*args, **kwargs))
            timeout_thread = TimeoutThread(timeout_seconds, executor_thread)
            timeout_thread.start()
            timeout_thread.join()
            if not timeout_thread.did_executor_thread_complete():
                raise timeout_thread.get_exception()
            else:
                exception = executor_thread.get_exception()
                if exception is not None:
                    raise exception
                return executor_thread.get_result()
        return wrapper
    return inner
