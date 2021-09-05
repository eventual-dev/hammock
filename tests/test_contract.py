import abc

import pytest

from tests.stack.abstract import StackInt
from tests.stack.linear import LinearStack


class StackContract(abc.ABC):
    def test_on_creation_is_empty(self, impl: StackInt) -> None:
        assert impl.is_empty

    def test_when_empty_size_is_zero(self, impl: StackInt) -> None:
        assert impl.size == 0

    def test_when_empty_peek_returns_none(self, impl: StackInt) -> None:
        assert impl.peek() is None

    def test_when_empty_pop_raises(self, impl: StackInt) -> None:
        with pytest.raises(IndexError):
            impl.pop()

    def test_after_push_not_empty(self, impl: StackInt) -> None:
        impl.push(None)
        assert not impl.is_empty

    def test_after_push_size_is_incremented(self, impl: StackInt) -> None:
        size = impl.size
        impl.push(None)
        assert impl.size == size + 1

    def test_after_push_peek_returns(self, impl: StackInt) -> None:
        value = "value"
        impl.push(value)
        assert impl.peek() is value

    def test_after_push_pop_returns(self, impl: StackInt) -> None:
        value = "value"
        impl.push(value)
        assert impl.pop() is value

    def test_after_push_pop_removes(self, impl: StackInt) -> None:
        value = "value"
        impl.push(value)
        impl.pop()
        assert impl.is_empty

    def test_after_pop_size_is_decremented(self, impl: StackInt) -> None:
        size = impl.size
        impl.push(None)
        impl.pop()
        assert impl.size == size


class TestLinearStackIsStack(StackContract):
    @pytest.fixture
    def impl(self) -> StackInt:
        return LinearStack()
