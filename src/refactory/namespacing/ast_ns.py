from __future__ import annotations

import ast

from ..log_utils import Console

__all__ = ["AstNamespace", "KwargName"]

logger = Console(name=__name__)


class AstNamespace:
    _namespace_prefix: str = "ast."

    @classmethod
    def namespace_cls_from_qualname(cls, qualname: str) -> type[ast.AST]:
        return vars(ast)[qualname.partition(".")[-1]]

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
        return AstNamespace.namespace_cls_from_qualname(ref) if is_ast else ref


class KwargName:
    def __init__(self, kw: str):
        self.kw = kw

    def __repr__(self) -> str:
        return f"{self.kw}**"

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.kw == other.kw

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))
