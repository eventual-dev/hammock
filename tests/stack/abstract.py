import abc
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class StackInt(Generic[T], abc.ABC):
    @abc.abstractmethod
    def peek(self) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def pop(self) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def push(self, value: T) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def size(self) -> int:
        raise NotImplementedError

    @property
    def is_empty(self) -> bool:
        return not bool(self.size)
