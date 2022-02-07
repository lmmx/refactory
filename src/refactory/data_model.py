from __future__ import annotations

import ujson
from pydantic import BaseModel
from pydantic.dataclasses import Field, dataclass

from ._types import AliasValTypes, RelType, Replacement
from .namespacing import Alias, AliasVal

__all__ = []


@dataclass  # (kw_only=True, slots=True)
class Preconditions:
    reltype: RelType  # = Field(default=None)
    # reltype: dict[str,str]


class RefactorRuleSpec(BaseModel):
    aliases: dict[Alias, AliasValTypes]
    preconditions: Preconditions
    replacement: Replacement = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def dump_json(self):
        # return ujson.dumps({"pages": [p.serialise() for p in self.pages]})
        return ujson.dumps({})  # TODO dump full spec

    @classmethod
    def from_dict(cls, spec: dict) -> RefactorRuleSpec:
        return cls(**spec)
