from __future__ import annotations

from pathlib import Path

from studio.core.delta_engine import DeltaEngine
from studio.calibration.map import CalibrationMap
from studio.detection.map_detector import MapDetector


class MapEngine:
    """
    BLAKKBOX Map Engine

    ORIGINAL
        │
        ▼
    MODIFIED
        │
        ▼
    Delta Engine
        │
        ▼
    Modified Regions
        │
        ▼
    Map Detector
        │
        ▼
    Classified Maps
    """

    def __init__(self):

        self.maps: list[CalibrationMap] = []

    def analyze(
        self,
        original: str | Path,
        modified: str | Path,
    ) -> list[CalibrationMap]:

        result = DeltaEngine.compare(
            original,
            modified,
        )

        rom = Path(modified).read_bytes()

        self.maps = MapDetector.detect(
            rom,
            result.regions,
        )

        return self.maps

    def clear(self):

        self.maps.clear()

    @property
    def count(self) -> int:

        return len(self.maps)

    def by_category(
        self,
        category: str,
    ) -> list[CalibrationMap]:

        return [
            m
            for m in self.maps
            if m.category.lower()
            == category.lower()
        ]

    def modified_maps(self) -> list[CalibrationMap]:

        return [
            m
            for m in self.maps
            if m.modified
        ]

    def summary(self) -> str:

        if not self.maps:

            return "No maps detected."

        categories = {}

        for m in self.maps:

            categories[m.category] = (
                categories.get(
                    m.category,
                    0,
                )
                + 1
            )

        lines = []

        lines.append(
            f"Detected Maps : {len(self.maps)}"
        )

        lines.append("")

        for category in sorted(categories):

            lines.append(
                f"{category:12} : {categories[category]}"
            )

        return "\n".join(lines)
