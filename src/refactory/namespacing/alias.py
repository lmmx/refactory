from __future__ import annotations

import ast

from .ast_ns import AstNamespace, KwargName
from .literal import string_literalify_if_denoted_else_kwarg

__all__ = ["Alias", "AliasVal"]


class Alias:
    _symbol = "!"

    def __init__(self, alias: str):
        self.idx = self.validate(alias)

    def validate(self, alias: str) -> int:
        prefix, sym, idx = alias.partition(self._symbol)
        if prefix or sym != self._symbol or not idx.isnumeric():
            raise TypeError(f"Alias {alias} does not start with '!'")
        return int(idx)

    def __repr__(self):
        return f"{self._symbol}{self.idx}"


class AliasVal:
    alias_val: str | dict | list

    def __init__(self, val: str | dict | list):
        if isinstance(val, str):
            self.alias_val = AstNamespace.nodify_if_in_ns(val)  # Just a string
        elif isinstance(val, dict):
            self.alias_val = ast_ref_tree(tree=val, init=True)  # AST all the way down
        elif isinstance(val, list):
            # An alias will never contain another alias
            # so you can always resolve the tree all the way to its leaf/leaves
            self.alias_val = [ast_ref_tree(tree=t, init=True) for t in val]  # Multiple
        else:
            raise TypeError(f"{val} is neither str, dict, or list type")

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
        processed_node = AstNamespace.nodify_if_in_ns(node)
        sub_is_kwarg = type(processed_node) is type and issubclass(
            processed_node, ast.AST
        )
        if not sub_is_kwarg:
            processed_node = KwargName(processed_node)
        # Recurse until reaching leaf of the AST ref tree
        if isinstance(subnode, dict):
            processed_subnode = ast_ref_tree(subnode)
            if sub_is_kwarg and any(
                type(k) is type and issubclass(k, ast.AST) for k in processed_subnode
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
