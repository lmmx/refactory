from __future__ import annotations

from dataclasses import dataclass, field

import ujson

from ._types import ASTTree, AliasDict, RelType
from .namespacing import Alias, AliasVal

__all__ = []


@dataclass(kw_only=True, slots=True)
class Preconditions:
    reltype: RelType = field(default=None)


Replacement_or_s = ASTTree | list[ASTTree]


@dataclass(init=False, slots=True)
class RefactorRuleSpec:
    aliases: AliasDict
    preconditions: Preconditions
    replacement: Replacement_or_s = field(default_factory=dict)

    def __init__(self, aliases: dict, preconditions: dict, replacement: dict):
        self.aliases = {repr(Alias(k)): AliasVal(v) for k, v in aliases.items()}
        self.preconditions = Preconditions(**preconditions)
        self.replacement = replacement

    def dump_json(self):
        # return ujson.dumps({"pages": [p.serialise() for p in self.pages]})
        return ujson.dumps({})  # TODO dump full spec

    @classmethod
    def from_dict(cls, spec: dict) -> RefactorRuleSpec:
        return cls(**spec)
