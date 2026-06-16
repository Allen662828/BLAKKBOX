from __future__ import annotations

from pathlib import Path

from studio.core.delta_engine import DeltaEngine
from studio.detection.map_detector import MapDetector
from studio.engine.map_engine import MapEngine


class DetectionEngine:
    """
    BLAKKBOX Detection Engine

        ORIGINAL.bin
              │
              ▼
        Delta Engine
              │
              ▼
        Modified Regions
              │
              ▼
        Map Detection
              │
              ▼
        Classification
    """

    def __init__(self):

        self.delta = None
        self.maps = []

    def detect(
        self,
        original: str | Path,
        modified: str | Path,
    ):

        self.delta = DeltaEngine.compare(
            original,
            modified,
        )

        rom = Path(modified).read_bytes()

        self.maps = MapDetector.detect(
            rom,
            self.delta.regions,
        )

        return self.maps

    @property
    def map_count(self):

        return len(self.maps)

    @property
    def region_count(self):

        if self.delta is None:
            return 0

        return len(self.delta.regions)

    @property
    def modified_bytes(self):

        if self.delta is None:
            return 0

        return len(self.delta.differences)

    def summary(self):

        if self.delta is None:

            return "No detection performed."

        lines = []

        lines.append("========== Detection ==========")
        lines.append(f"Regions        : {self.region_count}")
        lines.append(f"Modified Bytes : {self.modified_bytes}")
        lines.append(f"Detected Maps  : {self.map_count}")
        lines.append("")

        categories = {}

        for m in self.maps:

            categories[m.category] = (
                categories.get(
                    m.category,
                    0,
                )
                + 1
            )

        for category in sorted(categories):

            lines.append(
                f"{category:12} : {categories[category]}"
            )

        return "\n".join(lines)

    def clear(self):

        self.delta = None
        self.maps.clear()
