from dataclasses import dataclass, field
from typing import Any, Iterable, Type, TypeVar

from hammock.spec import MethodSpec
from hammock.spy import CallHistory

InterfaceType = TypeVar("InterfaceType", covariant=True)


@dataclass
class Patcher:
    call_history: CallHistory = field(default_factory=CallHistory)

    def mock(
        self,
        cls_to_patch: Type[InterfaceType],
        method_spec_seq: Iterable[MethodSpec],
    ) -> InterfaceType:
        base_cls = cls_to_patch.__base__

        abstract_method_name_set = getattr(base_cls, "__abstractmethods__", frozenset())

        cls_dict = {}
        for method_spec in method_spec_seq:
            attr = getattr(base_cls, method_spec.attr_name)
            method_call_history = (
                None if method_spec.count is None else self.call_history
            )
            cls_dict[method_spec.attr_name] = method_spec.wrap_attr(
                attr, call_history=method_call_history
            )

        def new_attr_fn(*args: Any, **kwargs: Any) -> Any:
            raise ValueError("this abstract method was not stubbed")

        for name in abstract_method_name_set - {
            method_spec.attr_name for method_spec in method_spec_seq
        }:
            cls_dict[name] = new_attr_fn

        cls_ = type("XXX", (base_cls,), cls_dict)
        return cls_()
