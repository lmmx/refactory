from __future__ import annotations

import ast

__all__ = ["Alias", "AliasVal", "RelPath"]


class Alias:
    _symbol = "!"

    def __init__(self, alias: str):
        self.idx = self.validate(alias)

    def validate(self, alias: str) -> int:
        prefix, sym, idx = alias.partition(self._symbol)
        if prefix or sym != self._symbol:
            raise TypeError(f"Alias {alias} does not start with '!'")
        if not idx.isnumeric():
            raise TypeError(f"Alias {alias} does not start with '!'")
        return int(idx)

    def __repr__(self):
        return f"{self._symbol}{self.idx}"


class AliasVal:
    alias_val: str | dict | list

    def __init__(self, val: str | dict | list):
        if isinstance(val, str):
            self.alias_val = ast_nodify_if_in_namespace(val)  # Just a string
        elif isinstance(val, dict):
            self.alias_val = ast_ref_tree(tree=val, init=True)  # AST all the way down
        elif isinstance(val, list):
            # An alias will never contain another alias
            # so you can always resolve the tree all the way to its leaf/leaves
            self.alias_val = [ast_ref_tree(tree=t, init=True) for t in val]  # Multiple
        else:
            raise TypeError(f"{alias_val} is neither str, dict, or list type")

    def serialise(self):
        if isinstance(self.alias_val, list):
            s = [ast_val.serialise() for ast_val in self.alias_val]
        if isinstance(self.alias_val, dict):
            s = self.alias_val.serialise()
        else:
            s = self.alias_val  # Return simple string without serialisation
        return s

    def __repr__(self) -> str:
        return f"{self.alias_val}"


class AstNamespace:
    _namespace_prefix: str = "ast."

    @classmethod
    def namespace_cls_from_qualname(cls, qualname: str) -> type[ast.stmt]:
        return vars(ast).get(qualname.partition(".")[-1])

    @classmethod
    def contains(cls, qualname: str) -> bool:
        """
        Validate a qualname e.g. ``ast.Assign`` by various prerequisited, before
        checking the module namespace itself if viable.
        """
        prefix, namespace, clsname = qualname.partition(cls._namespace_prefix)
        pre_validate = not prefix and namespace and clsname.isidentifier()
        return pre_validate and clsname in vars(ast)


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


class KwargName:
    def __init__(self, kw: str):
        self.kw = kw

    def __repr__(self) -> str:
        return f"{self.kw}*"


def ast_nodify_if_in_namespace(ref: str) -> type[ast.stmt] | str:
    is_ast = AstNamespace.contains(ref)
    return AstNamespace.namespace_cls_from_qualname(ref) if is_ast else ref


def string_literalify_if_denoted_else_kwarg(ref: str) -> StringLiteral | str:
    # NOTE: retval should probably have a class wrapping ref but IDK what so punting
    is_str_lit = StringLiteral.matches_format(ref)
    return StringLiteral.from_templated(ref) if is_str_lit else ref


def ast_ref_tree(tree: dict, init=False):
    """
    An AST tree starting at an AST node (without aliases), built from a dict
    in which the AST statement nodes are strings (hence the name 'ref' tree).
    Note that a single atomic node, built from a string, is not a tree.

    Codifying some logic here: an AST ref tree must be init'ed at an AST node (not a
    kwarg), so when init'ing a subnode tree beneath an AST node, give an indication of
    this by passing the ``init`` flag. Note that ``init`` does not mean 'root'.
    This then allows enforcement of some expectations, e.g. an AST node cannot be
    directly beneath another AST node (that's what AST kwarg names are for).
    """
    if not isinstance(tree, dict):
        raise TypeError(f"{tree} is not a dict so cannot be an AST reference tree")
    dereferenced_tree = {}
    for node, subnode in tree.items():
        processed_node = ast_nodify_if_in_namespace(node)
        sub_is_kwarg = (
            hasattr(processed_node, "mro") and ast.AST in processed_node.mro()
        )
        if not sub_is_kwarg:
            processed_node = KwargName(processed_node)
        # Recurse until reaching leaf of the AST ref tree
        if isinstance(subnode, dict):
            processed_subnode = ast_ref_tree(subnode)
            if sub_is_kwarg and any(
                hasattr(k, "mro") and ast.AST in k.mro() for k in processed_subnode
            ):
                raise TypeError(
                    f"Broken expectation: an AST statement {subnode=} was found "
                    f"directly beneath a previous AST node {node=}"
                )
        else:
            if sub_is_kwarg:  # if init and sub_is_kwarg:
                raise TypeError(
                    f"Broken expectation: leaf {subnode=} was found directly "
                    f"beneath a previous AST node {node=})"
                )
            # No need to check if leaf is AST node: can't be (need kwargs by definition)
            # but need to check if string literal (can only be leaves by definition)
            processed_subnode = string_literalify_if_denoted_else_kwarg(subnode)
        dereferenced_tree.update({processed_node: processed_subnode})
    return dereferenced_tree


class RelPath:
    _sep = "."

    def __init__(self, rel_path: str):
        self.path = self.validate(rel_path)

    @classmethod
    def is_valid_str(cls, rel_path: str) -> bool:
        return all(map(str.isidentifier, cls.split(rel_path)))

    @classmethod
    def split(cls, rel_path: str) -> tuple[str]:
        return tuple(rel_path.split(self._sep))

    def validate(self, rel_path: str) -> tuple[str]:
        if not self.is_valid_str(rel_path):
            raise TypeError(f"RelPath {rel_path} is not a valid node attribute path")
        return self.split(rel_path)

    def __repr__(self):
        return self._sep.join(self.path)
