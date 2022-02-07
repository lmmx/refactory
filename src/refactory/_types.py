from __future__ import annotations

from typing import Any, Dict, Union

from .namespacing.alias import Alias
from .namespacing.alias_val import AliasDictVal, AliasListVal, AliasStrVal
from .namespacing.ast_ns import AstStatement, KwargName
from .namespacing.bounce import BouncedRef
from .namespacing.rel import RelPath

__all__ = [
    "ASTTree",
    "AstRefTree",
    "AstStatement",
    #"AstStatementKwarg",
    "Precondition",
    "PreconditionDict",
    "PreconditionKind",
    "RelPrecondition",
    "RelType",
]

AliasValTypes = Union[AliasStrVal, AliasDictVal, AliasListVal]

# RelPath = str

# Alias should really be a generic, so as to specify that Alias is Alias[ast.AST]
RelType = Dict[RelPath, AstStatement | Alias]  # ``Alias[ast.AST]``

RelPrecondition = Dict[RelPath, AstStatement]

#AstStatement = str

# For now the only precondition implemented is `rel` isinstance validation
PreconditionKind = Union[RelType]
Precondition = Union[RelPrecondition]
PreconditionDict = Dict[PreconditionKind, Precondition]

AstStatementKwarg = str

AstRefTree = Union[Dict[str, str], Dict[str, Dict]]

_RecKey = Union[KwargName]#, AstStatement, Alias]
_RecVal = Union[Alias, BouncedRef, list[Alias]]

#RecursiveDict = Union[_RecVal, Dict[
#    _RecKey,
#    _RecVal,
#    #Union[_RecVal, Dict]
#]]
#RecursiveDict2x = Dict[
#    _RecKey, # "targets" or "value"
#    Union[str,dict]
#]

AstTreeKey = Union[AstStatement, Alias]
#AstTreeVal = Union[
#    RecursiveDict2x,
#    #Alias,
#]
AstTreeVal = Dict[
    Union[KwargName, str],
    _RecVal
]

ASTTree = Dict[AstTreeKey, AstTreeVal]

Replacement = list[ASTTree] #ASTTree | list[ASTTree]
