from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic
from threading import Thread


T = TypeVar('T')


class FunctionExecutor(Generic[T]):

    @abstractmethod
    def execute(self):
        pass


class FunctionResultContainer(Generic[T]):

    @abstractmethod
    def get_exception(self) -> Exception | None:
        pass

    @abstractmethod
    def get_result(self) -> T | None:
        pass


class CombinedExecutionContainer(Generic[T], FunctionExecutor[T], FunctionResultContainer[T], metaclass=ABCMeta):
    pass


class FunctionExecutorThread(Thread, FunctionResultContainer[T], Generic[T]):

    @abstractmethod
    def is_running(self) -> bool:
        pass
