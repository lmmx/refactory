from typing import Any, Dict, ForwardRef, List, Union

__all__ = [
    "ASTTree",
    "AliasDict",
    "AliasVal",
    "AstRefTree",
    "AstStatement",
    "AstStatementKwarg",
    "AstStatementKwargValue",
    "Precondition",
    "PreconditionDict",
    "PreconditionKind",
    "RelPrecondition",
    "RelType",
    "ValidatedAliasDict",
    "ValidatedAliasVal",
]

RelType = str

AstStatement = str

RelPrecondition = Dict[ForwardRef("RelPath"), AstStatement]

# For now the only precondition implemented is `rel` isinstance validation
PreconditionKind = Union[RelType]
Precondition = Union[RelPrecondition]
PreconditionDict = Dict[PreconditionKind, Precondition]

AstStatementKwarg = str

AstRefTree = Union[Dict[str, str], Dict[str, Dict]]
AliasVal = Union[str, ForwardRef("AstRefTree"), List[ForwardRef("AstRefTree")]]
AliasDict = Dict[ForwardRef("Alias"), AliasVal]
ValidatedAliasVal = Union[
    ForwardRef("RelPath"), ForwardRef("ASTTree"), List[ForwardRef("ASTTree")]
]
ValidatedAliasDict = Dict[ForwardRef("Alias"), ForwardRef("ValidatedAliasVal")]

AstStatementKwargValue = Any  # Temporary cop out! Annotate recursive types TODO
# ASTTree = Union[Dict[str, str], Dict[str, ForwardRef("ASTTree")]]
ASTTree = Dict[AstStatement, Dict[AstStatementKwarg, AstStatementKwargValue]]
