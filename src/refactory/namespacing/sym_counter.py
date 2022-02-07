from __future__ import annotations

from .validation import ValidatorBase

__all__ = ["SymbolCounter"]


class SymbolCounter(ValidatorBase):
    _symbol = NotImplemented # Must be overridden in subclass

    def __init__(self, ref: str):
        self.idx = self.idx_from_ref(ref)

    @classmethod
    def validate(cls, ref: str): # -> instance of class
        idx = cls.idx_from_ref(ref)
        return cls(f"{cls._symbol}{idx}")

    @classmethod
    def type_validate(cls, ref):
        if not isinstance(ref, str):
            raise TypeError(f"{cls.__name__} {ref} is not a string")

    @classmethod
    def parse_idx(cls, ref: str) -> int:
        prefix, sym, idx = ref.partition(cls._symbol)
        if prefix or sym != cls._symbol or not idx.isnumeric():
            raise TypeError(f"{cls.__name__} {ref} does not start with '{cls._symbol}'")
        return int(idx)

    @classmethod
    def idx_from_ref(cls, ref: str) -> int:
        cls.type_validate(ref)
        idx = cls.parse_idx(ref)
        return idx

    def __repr__(self):
        return f"{self._symbol}{self.idx}"

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.idx == other.idx

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))
