from dataclasses import dataclass, field
from typing import Any, Iterable, Type, TypeVar

from hammock import AttrContract, ReturnContract
from hammock.attr import AttrMock
from hammock.spy import CallHistory

InterfaceType = TypeVar("InterfaceType", covariant=True)


@dataclass
class Patcher:
    call_history: CallHistory = field(default_factory=CallHistory)

    def mock(
        self,
        cls_to_patch: Type[InterfaceType],
        attr_mock_seq: Iterable[AttrMock],
    ) -> InterfaceType:
        base_cls = cls_to_patch.__base__
        obj_with_contract = cls_to_patch()

        abstract_method_name_set = getattr(base_cls, "__abstractmethods__", frozenset())

        cls_dict = {}
        for attr_mock in attr_mock_seq:
            attr = getattr(base_cls, attr_mock.attr_name)
            method_call_history = None if attr_mock.count is None else self.call_history
            try:
                getattr(obj_with_contract, attr_mock.attr_name)
            except AttrContract as e:
                xs = [
                    contract.returns
                    for contract in e.call_contracts
                    if isinstance(contract, ReturnContract)
                ]
                if attr_mock.stub_with not in xs:
                    raise RuntimeError("not sure what to do")

            cls_dict[attr_mock.attr_name] = attr_mock.wrap_attr(
                attr, call_history=method_call_history
            )

        def new_attr_fn(*args: Any, **kwargs: Any) -> Any:
            raise ValueError("this abstract method was not stubbed")

        for name in abstract_method_name_set - {
            method_spec.attr_name for method_spec in attr_mock_seq
        }:
            cls_dict[name] = new_attr_fn

        cls_ = type("XXX", (base_cls,), cls_dict)
        return cls_()
