"""
delta/report.py

Delta analysis reporting.
"""

from __future__ import annotations

from core.logger import (
    section,
    kv,
)


class DeltaReport:
    """
    Reports delta analysis statistics.
    """

    def print(self, stats: dict) -> None:

        section("DELTA ANALYSIS")

        regions = stats.get("regions", 0)
        changed_bytes = stats.get("changed_bytes", 0)
        largest = stats.get("largest", 0)

        kv("Modified Regions", regions)
        kv("Changed Bytes", f"{changed_bytes:,}")
        kv("Largest Region", f"{largest:,} bytes")

        if regions > 0:

            average = changed_bytes / regions

            kv("Average Region Size", f"{average:.1f} bytes")

        else:

            kv("Average Region Size", "0 bytes")
