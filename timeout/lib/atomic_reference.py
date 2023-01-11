from typing import TypeVar, Generic

from threading import Lock


T = TypeVar('T')


class AtomicReference(Generic[T]):

    """
    A reference container that allows multiple threads to safely access or swap in a value.

    This does not make the underlying value being accessed or swapped in threadsafe. This merely provides a way
    for multiple threads to safely set or read said value from this reference.
    """

    def __init__(self, initial_value: T = None):
        """
        Initializes the atomic reference.

        :param initial_value: An optional value to initialize the value being stored by the atomic reference.
        """
        self._lock = Lock()
        self._value: T = initial_value

    def get_value(self) -> T | None:
        """
        Acquires the lock and returns the value held by this reference.

        :return: The current value of the container or None if no value has been set.
        """
        with self._lock:
            return self._value

    def set_value(self, value: T):
        """
        Acquires the lock and sets the value property of the atomic reference to the input value.

        :param value: The input value to store within the container.
        """
        with self._lock:
            self._value = value
