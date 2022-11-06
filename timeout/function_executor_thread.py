from typing import TypeVar, Generic, Callable

from .container import ValueContainer
from .function_executor import FunctionExecutorThread, CombinedExecutionContainer


T = TypeVar('T')


class PrimitiveFunctionExecutor(CombinedExecutionContainer[T], Generic[T]):

    def __init__(self, function: Callable[[], T]):
        self._function = function
        self._result = ValueContainer[T]()
        self._exception = ValueContainer[Exception]()

    def execute(self):
        try:
            result = self._function()
            self._result.set_value(result)
        except Exception as e:
            self._exception.set_value(e)

    def get_exception(self) -> Exception | None:
        return self._exception.get_value()

    def get_result(self) -> T | None:
        return self._result.get_value()


class PrimitiveFunctionExecutorThread(FunctionExecutorThread[T], Generic[T]):

    def __init__(self, executor: CombinedExecutionContainer[T]):
        super().__init__()
        self._executor = executor
        self._running = ValueContainer[bool](False)

    def run(self) -> None:
        self._running.set_value(True)
        self._executor.execute()
        self._running.set_value(False)

    def get_exception(self) -> Exception | None:
        return self._executor.get_exception()

    def get_result(self) -> T | None:
        return self._executor.get_result()

    def is_running(self) -> bool:
        return self._running.get_value()


def wrap_function_in_executor_thread(function: Callable[[], T]) -> FunctionExecutorThread[T]:
    executor = PrimitiveFunctionExecutor[T](function)
    return PrimitiveFunctionExecutorThread(executor)
