from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AnalysisReport:

    project: str

    version: str

    timestamp: str

    fingerprint: dict[str, Any] = field(default_factory=dict)

    delta: dict[str, Any] = field(default_factory=dict)

    classification: dict[str, Any] = field(default_factory=dict)

    axis: dict[str, Any] = field(default_factory=dict)

    geometry: dict[str, Any] = field(default_factory=dict)
