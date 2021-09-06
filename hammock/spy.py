from dataclasses import dataclass, field
from typing import Any, Callable, MutableMapping, Union

from hammock.util import name_from_attr


@dataclass
class CallHistory:
    call_count_from_method_name: MutableMapping[str, int] = field(default_factory=dict)

    def register_call(self, method_name: str) -> None:
        call_count = self.call_count_from_method_name.get(method_name, 0)
        self.call_count_from_method_name[method_name] = call_count + 1

    def count(self, method: Union[Callable[[Any], Any], property]) -> int:
        return self.call_count_from_method_name.get(name_from_attr(method), 0)
