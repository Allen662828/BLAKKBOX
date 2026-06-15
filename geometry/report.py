"""
geometry/report.py

Geometry analysis reporting.
"""

from __future__ import annotations

from collections import Counter

from configs.config import MAX_REPORT_CANDIDATES

from core.logger import (
    section,
    kv,
    info,
)


class GeometryReport:
    """
    Report geometry analysis statistics.
    """

    def print(self, tables: list[dict]) -> dict:

        total = len(tables)

        if total == 0:

            summary = {
                "total": 0,
                "valid": 0,
                "rejected": 0,
                "average_score": 0.0,
            }

            section("GEOMETRY ANALYSIS")

            kv("Candidates", 0)
            kv("Valid Tables", 0)
            kv("Rejected", 0)

            return summary

        # ------------------------------------------------------
        # Statistics
        # ------------------------------------------------------

        valid = sum(
            1
            for table in tables
            if table.get("valid", False)
        )

        rejected = total - valid

        average_score = (
            sum(
                table.get("score", 0)
                for table in tables
            )
            / total
        )

        summary = {
            "total": total,
            "valid": valid,
            "rejected": rejected,
            "average_score": average_score,
        }

        # ------------------------------------------------------
        # Main Summary
        # ------------------------------------------------------

        section("GEOMETRY ANALYSIS")

        kv("Candidates", total)
        kv("Valid Tables", valid)
        kv("Rejected", rejected)
        kv("Average Score", f"{average_score:.1f}")

        # ------------------------------------------------------
        # Shape Distribution
        # ------------------------------------------------------

        shape_counter = Counter()

        for table in tables:

            rows, cols = table.get(
                "shape",
                (0, 0)
            )

            shape_counter[f"{rows} x {cols}"] += 1

        if shape_counter:

            section("DETECTED SHAPES")

            for shape, count in sorted(shape_counter.items()):

                kv(shape, count)

        # ------------------------------------------------------
        # Top Candidates
        # ------------------------------------------------------

        ranked = sorted(
            tables,
            key=lambda table: table.get(
                "score",
                0
            ),
            reverse=True,
        )

        if ranked:

            section("TOP GEOMETRY CANDIDATES")

            for index, table in enumerate(
                ranked[:MAX_REPORT_CANDIDATES],
                start=1,
            ):

                rows, cols = table.get(
                    "shape",
                    (0, 0)
                )

                region = table.get("region")

                if region:

                    location = (
                        f"0x{region.start:08X}"
                        f"-"
                        f"0x{region.end:08X}"
                    )

                else:

                    location = "Unknown"

                info(
                    f"[{index}] "
                    f"{rows:>2}x{cols:<2} | "
                    f"Score={table.get('score', 0):>3} | "
                    f"{location}"
                )

        return summary
