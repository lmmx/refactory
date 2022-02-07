from __future__ import annotations

from .sym_counter import SymbolCounter

__all__ = ["BouncedRef"]


class BouncedRef(SymbolCounter):
    _symbol = "@"
