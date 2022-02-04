from __future__ import annotations

import ujson

from .data_model import RefactorRuleSpec
from .log_utils import Console

__all__ = ["load_spec"]

logger = Console(name=__name__).logger


def load_spec(spec: str) -> RefactorRuleSpec:
    if isinstance(spec, str):
        spec = ujson.loads(spec)
    if not isinstance(spec, dict):
        raise TypeError("Spec is not dict (JSON string)")
    rs = RefactorRuleSpec.from_dict(spec)
    return rs
