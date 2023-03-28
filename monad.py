# Imports # -------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import Iterable
from typing import Any, Literal



# Base Classes # --------------------------------------------------------------
@dataclass
class Monad:
    value: Any

    def unwrap(self) -> Any:
        return self.value

    def type(self) -> Any:
        return type(self.value)


class _ActualOrElseBase:
    def handle_bad_variant(self, not_ok) -> _ActualOrElseBase:
        pass


class _ApplyableBase:
    def apply(self, func) -> _ActualOrElseBase:
        try:
            if isinstance(self.value, Iterable):
                return type(self)([*map(func, self.value)])
            else:
                return type(self)(func(self.value))

        except Exception as e:
            return self.handle_bad_variant(e)



# The Actual Monads # ---------------------------------------------------------
@dataclass
class Maybe(Monad, _ActualOrElseBase, _ApplyableBase):
    variant: Literal["Ok", "Empty"] = field(init = False, repr = True)

    def __post_init__(self) -> None:
        if self.value is None:
            self.variant = "Empty"
        else:
            self.variant = "Ok"

    def handle_bad_variant(self, _) -> Maybe:
        return Maybe(None)


@dataclass
class Error(Monad, _ActualOrElseBase, _ApplyableBase):
    variant: Literal["Ok", "Error"] = field(init = False, repr = True)

    def __post_init__(self) -> None:
        if isinstance(self.value, Exception):
            self.variant = "Error"
        else:
            self.variant = "Ok"

    def handle_bad_variant(self, exception) -> Error:
        return Error(exception)
