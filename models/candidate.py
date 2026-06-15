from __future__ import annotations

from dataclasses import dataclass

from models.region import Region


@dataclass(slots=True)
class Candidate:

    score: int

    valid: bool

    rows: int

    columns: int

    region: Region | None = None

    confidence: float = 0.0

    @property
    def shape(self) -> tuple[int, int]:
        return self.rows, self.columns
