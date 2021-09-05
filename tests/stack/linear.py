from typing import List, Optional

from tests.stack.abstract import StackInt, T


class LinearStack(StackInt[T]):
    def __init__(self) -> None:
        self._contents: List[T] = []

    def peek(self) -> Optional[T]:
        return self._contents[-1] if self._contents else None

    def pop(self) -> T:
        return self._contents.pop()

    def push(self, value: T) -> None:
        self._contents.append(value)

    @property
    def size(self) -> int:
        return len(self._contents)
