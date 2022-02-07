from __future__ import annotations

import ast

from .ast_ns import AstNamespace, AstStatement, KwargName
from .literal import string_literalify_if_denoted_else_kwarg

__all__ = ["ast_ref_tree"]


def ast_ref_tree(tree: dict, init=False) -> dict:
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
        processed_node, processed_subnode = handle_tree_items(node, subnode)
        dereferenced_tree.update({processed_node: processed_subnode})
    return dereferenced_tree


def handle_tree_items(node, subnode):
    proc_node = AstStatement(node) if AstNamespace.contains(node) else KwargName(node)
    sub_is_kwarg = isinstance(proc_node, AstStatement)
    # Recurse until reaching leaf of the AST ref tree
    if isinstance(subnode, dict):
        proc_subnode = ast_ref_tree(subnode)
        if sub_is_kwarg and any(
            type(k) is type and issubclass(k, ast.AST) for k in proc_subnode
        ):
            raise TypeError(
                f"Broken expectation: an AST statement {subnode=} was found "
                f"directly beneath a previous AST node {node=}"
            )
    elif sub_is_kwarg:  # if init and sub_is_kwarg:
        raise TypeError(
            f"Broken expectation: leaf {subnode=} was found directly "
            f"beneath a previous AST node {node=})"
        )
    else:
        # No need to check if leaf is AST node: can't be (need kwargs by definition)
        # but need to check if string literal (can only be leaves by definition)
        proc_subnode = string_literalify_if_denoted_else_kwarg(subnode)
    return proc_node, proc_subnode
