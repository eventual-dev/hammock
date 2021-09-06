from typing import Any


def name_from_attr(attr: Any) -> str:
    if isinstance(attr, property) and attr.fget is not None:
        return attr.fget.__name__
    return attr.__name__
