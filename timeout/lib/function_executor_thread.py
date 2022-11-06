from typing import TypeVar, Generic, Callable

from .atomic_reference import AtomicReference
from .function_executor import FunctionExecutorThread, CombinedExecutionContainer
from .. import FunctionResultContainer

T = TypeVar('T')


class PrimitiveFunctionExecutor(CombinedExecutionContainer[T], Generic[T]):

    """
    A bare-bones implementation of a CombinedExecutionContainer. This implementation simply takes in a single niladic
    function, executes it, and captures either the output of the function or an exception if one was raised by said
    function.

    The result or exception of the underlying function are housed in AtomicReferences and, as such, can be
    accessed in a threadsafe manner.
    """

    def __init__(self, function: Callable[[], T]):
        self._function = function
        self._result = AtomicReference[T]()
        self._exception = AtomicReference[Exception]()

    def execute(self):
        try:
            result = self._function()
            self._result.set_value(result)
        except Exception as e:
            self._exception.set_value(e)

    def get_exception(self) -> Exception | None:
        return self._exception.get_value()

    def get_return_value(self) -> T | None:
        return self._result.get_value()


class PrimitiveFunctionExecutorThread(FunctionExecutorThread[T], Generic[T]):

    """
    A bare-bones implementation of a FunctionExecutorThread.
    """

    def __init__(self, executor: CombinedExecutionContainer[T]):
        super().__init__()
        self._executor = executor
        self._running = AtomicReference[bool](False)

    def run(self) -> None:
        self._running.set_value(True)
        self._executor.execute()
        self._running.set_value(False)

    def get_execution_result(self) -> FunctionResultContainer[T]:
        return self._executor

    def is_running(self) -> bool:
        return self._running.get_value()


def wrap_function_in_executor_thread(function: Callable[[], T]) -> FunctionExecutorThread[T]:
    executor = PrimitiveFunctionExecutor[T](function)
    return PrimitiveFunctionExecutorThread(executor)
