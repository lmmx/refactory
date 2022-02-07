from __future__ import annotations

from .validation import ValidatorBase

__all__ = ["RelPath"]


class RelPath(ValidatorBase):
    _sep = "."

    def __init__(self, rel_path: str):
        self.validate_path(rel_path)
        self.path = self.split(rel_path)

    @classmethod
    def is_valid_str(cls, rel_path: str) -> bool:
        return all(map(str.isidentifier, cls.split(rel_path)))

    @classmethod
    def split(cls, rel_path: str) -> tuple[str]:
        return tuple(rel_path.split(cls._sep))

    @classmethod
    def validate_path(cls, rel_path: str):
        """Permit the empty string (the identity) else check each 'part' of the path"""
        if rel_path and not cls.is_valid_str(rel_path):
            raise TypeError(f"RelPath {rel_path} is not a valid node attribute path")

    @classmethod
    def validate(cls, rel_path: str) -> str:
        cls.validate_path(rel_path)
        return cls(rel_path)

    def __repr__(self) -> str:
        return f":{self._sep.join(self.path)}"

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.path == other.path

    def __hash__(self) -> hash:
        return hash(tuple(sorted(vars(self).items())))

