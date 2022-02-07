from __future__ import annotations

from .validation import ValidatorBase

__all__ = ["Alias"]


class Alias(ValidatorBase):
    _symbol = "!"

    def __init__(self, alias: str):
        self.idx = self.idx_from_alias(alias)

    @classmethod
    def validate(cls, alias: str) -> Alias:
        idx = cls.idx_from_alias(alias)
        return cls(f"!{idx}")

    @classmethod
    def idx_from_alias(cls, alias: str) -> int:
        prefix, sym, idx = alias.partition(cls._symbol)
        if prefix or sym != cls._symbol or not idx.isnumeric():
            raise TypeError(f"Alias {alias} does not start with '!'")
        return int(idx)

    def __repr__(self):
        return f"{self._symbol}{self.idx}"

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.idx == other.idx

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))
