import abc
from typing import Any, Iterable, Optional, Type, TypeVar

from hammock.control import MockControl
from hammock.spec import MethodSpec

InterfaceType = TypeVar("InterfaceType")


class MockMeta(abc.ABCMeta):
    def set_up(
        cls: Type[InterfaceType],
        method_spec_seq: Iterable[MethodSpec],
        control: Optional[MockControl] = None,
    ) -> InterfaceType:
        base_cls = cls.__base__

        abstract_method_name_set = getattr(base_cls, "__abstractmethods__", frozenset())

        call_history = None if control is None else control.call_history

        x = {}
        for method_spec in method_spec_seq:
            attr = getattr(base_cls, method_spec.attr_name)
            method_call_history = None if method_spec.count is None else call_history
            x[method_spec.attr_name] = method_spec.wrap_attr(
                attr, call_history=method_call_history
            )

        def new_attr_(*args: Any, **kwargs: Any) -> Any:
            raise ValueError("this abstract method was not stubbed")

        for name in abstract_method_name_set - {
            method_spec.attr_name for method_spec in method_spec_seq
        }:
            x[name] = new_attr_

        cls_ = type("XXX", (base_cls,), x)
        return cls_()
