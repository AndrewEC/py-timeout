from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic
from threading import Thread


T = TypeVar('T')


class FunctionExecutor(Generic[T]):

    @abstractmethod
    def execute(self):
        """
        Instructs the underlying implementation to execute an underlying function. This strictly deals with the
        execution of an underlying function and not necessarily the capture of the function's output.
        """
        pass


class FunctionResultContainer(Generic[T]):

    """
    A container allowing one to access the result of the execution of an underlying function. The result could
    either be a concrete value returned by said function or an exception that was raised during the function's
    execution.
    """

    @abstractmethod
    def get_exception(self) -> Exception | None:
        """
        Returns the exception that was raised and captured during the execution of an underlying function.

        The return value of this function can be None. If the return value is None then it indicates the
        underlying function executed "successfully" and exited without raising anything.

        :return: The exception captured during the execution of an underlying function, or None if no exception was
            captured.
        """
        pass

    @abstractmethod
    def get_return_value(self) -> T | None:
        """
        Returns the value that was returned by an underlying function and subsequently captured.

        The return value can be None if the value returned from the underlying function is None or if the
        underlying function raised an exception. Therefore, if one wishes to identify if the underlying function
        successfully executed or not it would be best to inspect the value returned by get_exception for
        truthiness instead.

        :return: The value originally returned by the underlying function.
        """
        pass


class CombinedExecutionContainer(Generic[T], FunctionExecutor[T], FunctionResultContainer[T], metaclass=ABCMeta):
    """
    When used allows one to execute an underlying function, capture its result, and retrieve said result.
    """
    pass


class FunctionExecutorThread(Thread, Generic[T]):

    """
    When used allows one to execute an underlying function, capture its result, and retrieve said result within
    the context of a separate running thread.
    """

    @abstractmethod
    def get_execution_result(self) -> FunctionResultContainer[T]:
        """
        Returns the function result container containing the result of the execution of the underlying function.

        :return: A container that contains and exposes the result of the execution of an underlying function.
        """
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """
        Indicates if the thread is currently running.

        :return: True if the thread is currently running, otherwise false.
        """
        pass
