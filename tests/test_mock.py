from typing import Optional

import hammock
from tests.stack.abstract import StackInt


class MockStack(StackInt[str]):
    def peek(self) -> Optional[str]:
        raise

    def pop(self) -> str:
        raise

    def push(self, value: str) -> None:
        raise

    @property
    def size(self) -> int:
        raise


def test_stack_mock() -> None:
    patcher = hammock.Patcher()
    stack_mock = patcher.mock(
        MockStack,
        [
            hammock.MethodSpec(
                method=StackInt.peek,
                stub_with="value",
                count=True,
            ),
            hammock.MethodSpec(
                method=StackInt.size,
                stub_with=10,
            ),
        ],
    )
    assert stack_mock.peek() == "value"
    assert stack_mock.size == 10
    assert not stack_mock.is_empty

    assert patcher.call_history.count(StackInt.size) == 2
