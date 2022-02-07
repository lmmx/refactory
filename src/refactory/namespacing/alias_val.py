from __future__ import annotations

from inspect import get_annotations

from .ast_ns import AstNamespace, AstStatement
from .ast_ref import ast_ref_tree
from .validation import ValidatorBase

__all__ = ["AliasVal"]


class AliasVal(ValidatorBase):
    # Note: RelPath is not currently implemented in AliasVal but could be in future

    def __init__(self, val: str):
        self.alias_val = self.resolve_val(val)

    @classmethod
    def resolve_val(cls, val):
        raise NotImplementedError("Override resolve_val method in AliasVal subclass")

    @classmethod
    def type_validate(cls, val):
        annotated_val_type = get_annotations(cls, eval_str=True)["alias_val"]
        if not isinstance(val, annotated_val_type):
            raise TypeError(f"{val} type is not a {annotated_val_type}")

    @classmethod
    def validate(cls, val: str | dict | list) -> type[AliasVal]:
        cls.type_validate(val)  # Type validate
        return cls(val)

    def __repr__(self) -> str:
        return f"{self.alias_val}"

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.alias_val == other.alias_val


class AliasStrVal(AliasVal):
    alias_val: str

    @classmethod
    def resolve_val(cls, val: str) -> AstStatement | str:
        return AstStatement(val) if AstNamespace.contains(val) else val

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))


class AliasDictVal(AliasVal):
    alias_val: dict

    @classmethod
    def resolve_val(cls, val: dict) -> dict:
        return ast_ref_tree(tree=val, init=True)  # AST all the way down

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))


class AliasListVal(AliasVal):
    alias_val: list

    @classmethod
    def resolve_val(cls, val: list) -> list[dict]:
        """
        An alias will never contain another alias so you can always resolve the tree
        all the way to its leaf/leaves
        """
        return [ast_ref_tree(tree=t, init=True) for t in val]  # Multiple

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))
