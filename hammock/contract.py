from dataclasses import dataclass
from typing import Any, Generic, Mapping, Tuple, TypeVar

ReturnType = TypeVar("ReturnType")


@dataclass(frozen=True)
class CallContract(Generic[ReturnType]):
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]


@dataclass(frozen=True)
class ReturnContract(CallContract[ReturnType]):
    returns: ReturnType


@dataclass(frozen=True)
class RaiseContract(CallContract):
    raises: Exception


class AttrContract(Exception, Generic[ReturnType]):
    def __init__(self, *args: CallContract[ReturnType]) -> None:
        self.call_contracts = args
