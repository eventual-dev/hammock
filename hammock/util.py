from typing import Any


def name_from_attr(attr: Any) -> str:
    if isinstance(attr, property):
        return attr.fget.__name__
    return attr.__name__
