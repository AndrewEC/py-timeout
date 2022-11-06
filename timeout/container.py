from typing import TypeVar, Generic

from threading import Lock


T = TypeVar('T')


class ValueContainer(Generic[T]):

    def __init__(self, initial_value: T = None):
        self._lock = Lock()
        self._value: T = initial_value

    def get_value(self) -> T | None:
        with self._lock:
            return self._value

    def set_value(self, value: T):
        with self._lock:
            self._value = value
