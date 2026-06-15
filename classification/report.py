"""
classification/report.py

Region classification reporting.
"""

from __future__ import annotations

from core.logger import (
    section,
    kv,
)


class ClassificationReport:
    """
    Report classification statistics.
    """

    def print(self, regions) -> dict:

        calibration = 0
        unknown = 0
        small = 0

        total_confidence = 0.0

        for region in regions:

            total_confidence += getattr(
                region,
                "confidence",
                0.0
            )

            region_type = getattr(
                region,
                "region_type",
                "UNKNOWN"
            )

            if region_type == "CALIBRATION":

                calibration += 1

            elif region_type == "SMALL_EDIT":

                small += 1

            else:

                unknown += 1

        total = len(regions)

        average_confidence = (
            total_confidence / total
            if total
            else 0.0
        )

        summary = {
            "total": total,
            "calibration": calibration,
            "unknown": unknown,
            "small": small,
            "average_confidence": average_confidence,
        }

        section("REGION CLASSIFICATION")

        kv("Total Regions", summary["total"])
        kv("Calibration Regions", summary["calibration"])
        kv("Unknown Regions", summary["unknown"])
        kv("Small Regions", summary["small"])
        kv(
            "Average Confidence",
            f"{summary['average_confidence']:.2f}"
        )

        return summary
