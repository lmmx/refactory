from __future__ import annotations

__all__ = ["RelPath"]


class RelPath:
    _sep = "."

    def __init__(self, rel_path: str):
        self.path = self.validate(rel_path)

    @classmethod
    def is_valid_str(cls, rel_path: str) -> bool:
        return all(map(str.isidentifier, cls.split(rel_path)))

    @classmethod
    def split(cls, rel_path: str) -> tuple[str]:
        return tuple(rel_path.split(cls._sep))

    def validate(self, rel_path: str) -> tuple[str]:
        if not self.is_valid_str(rel_path):
            raise TypeError(f"RelPath {rel_path} is not a valid node attribute path")
        return self.split(rel_path)

    def __repr__(self):
        return self._sep.join(self.path)
