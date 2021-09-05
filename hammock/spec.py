from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeVar, Union

from hammock.control import CallHistory
from hammock.util import name_from_attr

InterfaceType = TypeVar("InterfaceType")


@dataclass(frozen=True)
class MethodSpec:
    method: Union[Callable[[InterfaceType], Any], property]
    stub_with: Any
    count: bool = False

    @property
    def attr_name(self) -> str:
        return name_from_attr(self.method)

    def wrap_attr(self, attr: Any, call_history: Optional[CallHistory]) -> Any:
        # fn = attr.fget if isinstance(attr, property) else attr

        # @wraps(fn)
        def new_attr_(*args: Any, **kwargs: Any) -> Any:
            return self.stub_with

        def new_attr_with_call_history_(*args: Any, **kwargs: Any) -> Any:
            call_history.register_call(self.attr_name)  # type: ignore
            return self.stub_with

        new_attr = new_attr_ if call_history is None else new_attr_with_call_history_
        return property(new_attr) if isinstance(attr, property) else new_attr
