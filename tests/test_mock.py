from typing import Optional

import hammock
from hammock import AttrContract, ReturnContract
from tests.stack.abstract import StackInt


class MockStack(StackInt[str]):
    def peek(self) -> Optional[str]:
        raise AttrContract[Optional[str]](
            ReturnContract(args=(), kwargs={}, returns="value"),
        )

    def pop(self) -> str:
        raise

    def push(self, value: str) -> None:
        raise

    @property
    def size(self) -> int:
        raise AttrContract[int](ReturnContract(args=(), kwargs={}, returns=10))


def test_stack_mock() -> None:
    patcher = hammock.Patcher()
    stack_mock = patcher.mock(
        MockStack,
        [
            hammock.AttrMock(
                attr=StackInt.peek,
                stub_with="value",
                count=True,
            ),
            hammock.AttrMock(
                attr=StackInt.size,
                stub_with=10,
            ),
        ],
    )
    assert stack_mock.peek() == "value"
    assert stack_mock.size == 10
    assert not stack_mock.is_empty

    assert patcher.call_history.count(StackInt.size) == 2
