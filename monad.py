from __future__ import annotations
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any, Literal

@dataclass
class Monad:
    value: Any

    def unwrap(self) -> Any:
        return self.value

    def type(self) -> Any:
        return type(self.value)


@dataclass
class ActualOrElse:
    def map(self, func) -> Maybe:
        try:
            if isinstance(self.value, Iterable):
                return Maybe([*map(func, self.value)])
            else:
                return Maybe(*map(func, [self.value]))

        except Exception as e:
            match self:
                case Maybe():
                    return Maybe(None)
                case Error():
                    return Error(e)
                case _:
                    raise NotImplementedError


@dataclass
class Maybe(Monad, ActualOrElse):
    variant: Literal["Ok", "Empty"] = field(init = False, repr = True)

    def __post_init__(self):
        if self.value is None:
            self.variant = "Empty"
        else:
            self.variant = "Ok"

@dataclass
class Error(Monad, ActualOrElse):
    variant: Literal["Ok", "Error"] = field(init = False, repr = True)

    def __post_init__(self):
        if isinstance(self.value, Exception):
            self.variant = "Error"
        else:
            self.variant = "Ok"