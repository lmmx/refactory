from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Type, Union, Any

import ujson
from dataclass_wizard import JSONWizard

__all__ = []


@dataclass
class Alias:
    alias: str


@dataclass
class RelPath:
    path: str


@dataclass
class ASTTree:
    pass  # Annotate recursive types TODO


@dataclass
class AstStatement:
    pass  # Annotate recursive types TODO


@dataclass
class AstStatementKwarg:
    pass  # Annotate recursive types TODO


Aliases = Dict[Alias, Union[RelPath, ASTTree, List[ASTTree]]]
RelType = Dict[RelPath, AstStatement]
AstStatementKwargValue = Any # Temporary cop out! Annotate recursive types TODO
ASTTree = Dict[AstStatement, Dict[AstStatementKwarg, AstStatementKwargValue]]


@dataclass
class Aliases:
    aliases: Aliases


@dataclass
class Preconditions:
    reltype: RelType


@dataclass
class Replacement:
    reltype: ASTTree | list[ASTTree]


@dataclass
class RefactorRuleSpec(JSONWizard):
    aliases: Aliases
    preconditions: Preconditions
    replacement: Replacement

    class _(JSONWizard.Meta):
        # Sets the target key transform to use for serialization;
        # defaults to `camelCase` if not specified.
        key_transform_with_dump = "SNAKE"

    def dump_json(self):
        # return ujson.dumps({"pages": [p.serialise() for p in self.pages]})
        return ujson.dumps({})  # TODO dump full spec
