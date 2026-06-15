"""
delta/merger.py

Merge adjacent regions into larger contiguous regions.

Two neighbouring regions are merged when the byte gap between
them is less than or equal to the configured merge threshold.
"""

from __future__ import annotations

from configs.config import MERGE_MAX_GAP

from delta.region import DeltaRegion

from core.logger import (
    section,
    kv,
)


class DeltaMerger:
    """
    Merge neighbouring regions into larger contiguous regions.
    """

    def __init__(self, max_gap: int | None = None) -> None:

        self.max_gap = MERGE_MAX_GAP if max_gap is None else max_gap

    def merge(self, regions: list[DeltaRegion]) -> list[DeltaRegion]:

        if not regions:
            return []

        ordered = sorted(regions, key=lambda region: region.start)

        merged: list[DeltaRegion] = []

        current = DeltaRegion(
            start=ordered[0].start,
            end=ordered[0].end,
        )

        for region in ordered[1:]:

            gap = region.start - current.end - 1

            if gap <= self.max_gap:

                current.end = max(
                    current.end,
                    region.end,
                )

            else:

                merged.append(current)

                current = DeltaRegion(
                    start=region.start,
                    end=region.end,
                )

        merged.append(current)

        return merged

    def statistics(
        self,
        before: list[DeltaRegion],
        after: list[DeltaRegion],
    ) -> dict:
        """
        Generate and display merge statistics.

        Returns
        -------
        dict
            Dictionary containing merge statistics.
        """

        original_count = len(before)
        merged_count = len(after)

        reduction = original_count - merged_count

        reduction_pct = (reduction / original_count) * 100.0 if original_count else 0.0

        average_length = (
            sum(region.length for region in after) / merged_count
            if merged_count
            else 0.0
        )

        stats = {
            "merge_gap": self.max_gap,
            "original_regions": original_count,
            "merged_regions": merged_count,
            "reduction": reduction,
            "reduction_pct": reduction_pct,
            "average_region_length": average_length,
        }

        section("REGION MERGER")

        kv("Merge Gap", f"{stats['merge_gap']} bytes")
        kv("Original Regions", stats["original_regions"])
        kv("Merged Regions", stats["merged_regions"])
        kv("Reduction", stats["reduction"])
        kv("Reduction %", f"{stats['reduction_pct']:.1f}%")
        kv(
            "Average Region Length",
            f"{stats['average_region_length']:.1f} bytes",
        )

        return stats
