from __future__ import annotations

from .sym_counter import SymbolCounter

__all__ = ["Alias"]


class Alias(SymbolCounter):
    _symbol = "!"
