import hammock
from tests.stack.abstract import StackInt


class MockStack(StackInt[str], metaclass=hammock.MockMeta):
    pass


def test_stack_mock() -> None:
    mock_control = hammock.MockControl()
    stack_mock = MockStack.set_up(
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
        mock_control,
    )
    assert stack_mock.peek() == "value"
    assert stack_mock.size == 10
    assert not stack_mock.is_empty

    assert mock_control.call_history.count(StackInt.size) == 2
