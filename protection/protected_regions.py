"""Protected-region enforcement for BLAKKBOX exports."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ProtectedRange:
    start: int
    end: int
    label: str = "protected"

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError(f"Invalid protected range: {self.start:#x}-{self.end:#x}")

    def contains(self, offset: int) -> bool:
        return self.start <= offset <= self.end


@dataclass(slots=True)
class ProtectedHit:
    offset: int
    label: str

    def as_dict(self) -> dict[str, str | int]:
        return {"offset": self.offset, "offset_hex": f"0x{self.offset:X}", "label": self.label}


class ProtectedRegionGuard:
    """Reject filtered deltas that touch policy-protected offsets."""

    def __init__(self, ranges: list[ProtectedRange] | None = None) -> None:
        self.ranges = ranges or []

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProtectedRegionGuard":
        ranges: list[ProtectedRange] = []
        for item in data.get("ranges", []) or []:
            if not isinstance(item, dict):
                continue
            ranges.append(
                ProtectedRange(
                    start=int(str(item["start"]), 0),
                    end=int(str(item["end"]), 0),
                    label=str(item.get("label", "protected")),
                )
            )
        return cls(ranges)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ProtectedRegionGuard":
        config_path = Path(path)
        if not config_path.exists():
            return cls()
        try:
            import yaml  # type: ignore[import-not-found]
        except Exception:
            return cls()
        with config_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            return cls()
        return cls.from_dict(data)

    def find_hits(self, offsets: set[int] | dict[int, int]) -> list[ProtectedHit]:
        keys = set(offsets.keys()) if isinstance(offsets, dict) else set(offsets)
        hits: list[ProtectedHit] = []
        for offset in sorted(keys):
            for protected_range in self.ranges:
                if protected_range.contains(offset):
                    hits.append(ProtectedHit(offset=offset, label=protected_range.label))
                    break
        return hits

    def validate(self, offsets: set[int] | dict[int, int]) -> list[ProtectedHit]:
        hits = self.find_hits(offsets)
        if hits:
            sample = ", ".join(f"0x{hit.offset:X}:{hit.label}" for hit in hits[:10])
            raise RuntimeError(f"Filtered delta touches protected region(s): {sample}")
        return hits
