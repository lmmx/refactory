from __future__ import annotations

__all__ = ["StringLiteral"]


class StringLiteral:
    _format_pre: str = "${"
    _format_suf: str = "}"

    def __init__(self, literal: str):
        self.literal: str = literal

    def __repr__(self) -> str:
        return f"`{self._format_pre}{self.literal}{self._format_suf}`"

    @classmethod
    def from_templated(cls, templated: str) -> StringLiteral:
        inner_literal = templated[len(cls._format_pre) : -len(cls._format_suf)]
        return cls(inner_literal)

    @classmethod
    def matches_format(cls, templated: str) -> bool:
        """
        Validate a qualname e.g. ``ast.Assign`` by various prerequisited, before
        checking the module namespace itself if viable.
        """
        pre_validate = templated.startswith(cls._format_pre)
        suf_validate = templated.endswith(cls._format_suf)
        return pre_validate and suf_validate

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.literal == other.literal

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))


def string_literalify_if_denoted_else_kwarg(ref: str) -> StringLiteral | str:
    # NOTE: retval should probably have a class wrapping ref but IDK what so punting
    is_str_lit = StringLiteral.matches_format(ref)
    return StringLiteral.from_templated(ref) if is_str_lit else ref
