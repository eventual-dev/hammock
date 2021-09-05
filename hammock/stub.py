from typing import Any, Iterable, Optional


class StubContract(Exception):
    def __init__(
        self,
        *,
        can_return: Optional[Iterable[Any]],
    ) -> None:
        self.returns = can_return
