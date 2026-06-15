from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Region:

    start: int
    end: int

    region_type: str = "UNKNOWN"

    confidence: float = 0.0

    calibration: bool = False

    @property
    def length(self) -> int:
        return self.end - self.start + 1
