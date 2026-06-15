from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GeometrySummary:

    total: int = 0

    valid: int = 0

    rejected: int = 0

    average_score: float = 0.0
