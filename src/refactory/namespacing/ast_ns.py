from __future__ import annotations

import ast

from ..log_utils import Console
from .validation import ValidatorBase

__all__ = ["AstNamespace", "AstStatement", "KwargName"]

logger = Console(name=__name__)


class AstNamespace:
    _ns_name: str = "ast"
    _namespace_prefix: str = f"{_ns_name}."

    @classmethod
    def ns_cls_from_name(cls, name: str) -> type[ast.AST]:
        """Works with either a pathname (e.g. ``ast.If``) or qualname (e.g. ``If``)"""
        return vars(ast)[name.partition(".")[-1]]

    @classmethod
    def contains(cls, pathname: str) -> bool:
        """
        Validate a qualname e.g. ``Assign`` from its pathname (e.g. ``ast.Assign``) by
        syntax prerequisites, before checking the qualname is in the module namespace.
        Note the meth:`str.isidentifier()` check will exclude multi-level qualnames.
        """
        prefix, namespace, qualname = pathname.partition(cls._namespace_prefix)
        pre_validate = not prefix and namespace and qualname.isidentifier()
        return pre_validate and qualname in vars(ast)

    @classmethod
    def nodify_if_in_ns(cls, ref: str) -> type[ast.AST] | str:
        is_ast = cls.contains(ref)
        return AstNamespace.ns_cls_from_name(ref) if is_ast else ref


class AstStatement(ValidatorBase):
    """Should be refactored so that `from_pathname` becomes a classmethod not init"""

    def __init__(self, pathname: str):
        self.validate_name(pathname)
        self.qualname = self.qualname_from_pathname(pathname)
        self.ns_node = AstNamespace.ns_cls_from_name(pathname)

    @classmethod
    def validate_name(cls, pathname: str):
        if not AstNamespace.contains(pathname):
            raise TypeError(
                f"{pathname} is not a top-level path in the `ast` module namespace"
            )

    @classmethod
    def qualname_from_pathname(cls, pathname: str) -> str:
        return pathname.partition(AstNamespace._namespace_prefix)[-1]

    @classmethod
    def validate(cls, pathname: str) -> str:
        cls.validate_name(pathname)
        qualname = cls.qualname_from_pathname(pathname)
        return cls(f"ast.{qualname}")

    def __repr__(self) -> str:
        return f"ast⠶{self.qualname}"

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.qualname == other.qualname

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))


class KwargName:
    def __init__(self, kw: str):
        self.kw = kw

    def __repr__(self) -> str:
        return f"{self.kw}**"

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.kw == other.kw

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))
