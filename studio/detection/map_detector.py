from __future__ import annotations

from pathlib import Path

from studio.calibration.map import CalibrationMap
from studio.core.region import Region
from studio.detection.map_classifier import MapClassifier


class MapDetector:
    """
    First-generation DENSO map detector.

    Detects candidate calibration maps from modified regions.

    Future versions will add:

        • Axis detection
        • Gradient analysis
        • Entropy scoring
        • Table smoothness
        • OEM signatures
        • KD/GD/YD/4N15 specific heuristics
    """

    DEFAULT_ROWS = 16
    DEFAULT_COLUMNS = 16
    DEFAULT_ELEMENT_SIZE = 2

    @staticmethod
    def detect(
        rom: bytes,
        regions: list[Region],
    ) -> list[CalibrationMap]:

        maps: list[CalibrationMap] = []

        for region in regions:

            if region.length < 64:
                continue

            address = region.start

            candidate = CalibrationMap(
                name="Unknown",
                address=address,
                rows=MapDetector.DEFAULT_ROWS,
                columns=MapDetector.DEFAULT_COLUMNS,
                element_size=MapDetector.DEFAULT_ELEMENT_SIZE,
            )

            MapClassifier.classify(candidate)

            candidate.modified = True

            maps.append(candidate)

        return maps

    @staticmethod
    def detect_file(
        filename: str | Path,
        regions: list[Region],
    ) -> list[CalibrationMap]:

        data = Path(filename).read_bytes()

        return MapDetector.detect(
            data,
            regions,
        )

    @staticmethod
    def modified_only(
        maps: list[CalibrationMap],
    ) -> list[CalibrationMap]:

        return [
            m
            for m in maps
            if m.modified
        ]

    @staticmethod
    def by_category(
        maps: list[CalibrationMap],
        category: str,
    ) -> list[CalibrationMap]:

        return [
            m
            for m in maps
            if m.category.lower()
            == category.lower()
        ]
