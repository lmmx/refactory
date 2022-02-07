from __future__ import annotations

from typing import Any, Dict, Union

from .namespacing.alias import Alias
from .namespacing.alias_val import AliasDictVal, AliasListVal, AliasStrVal
from .namespacing.ast_ns import AstStatement

__all__ = [
    "ASTTree",
    "AstRefTree",
    "AstStatement",
    "AstStatementKwarg",
    "AstStatementKwargValue",
    "Precondition",
    "PreconditionDict",
    "PreconditionKind",
    "RelPrecondition",
    "RelType",
]

AliasValTypes = Union[AliasStrVal, AliasDictVal, AliasListVal]

RelPath = str

# Alias should really be a generic, so as to specify that Alias is Alias[ast.AST]
RelType = Dict[RelPath, AstStatement | Alias]  # ``Alias[ast.AST]``

AstStatement = str

RelPrecondition = Dict[RelPath, AstStatement]

# For now the only precondition implemented is `rel` isinstance validation
PreconditionKind = Union[RelType]
Precondition = Union[RelPrecondition]
PreconditionDict = Dict[PreconditionKind, Precondition]

AstStatementKwarg = str

AstRefTree = Union[Dict[str, str], Dict[str, Dict]]

AstStatementKwargValue = Any  # Temporary cop out! Annotate recursive types TODO

ASTTree = Dict[AstStatement, Dict[AstStatementKwarg, AstStatementKwargValue]]
# Replacement_or_s = ASTTree | list[ASTTree]
Replacement = ASTTree | list[ASTTree]
