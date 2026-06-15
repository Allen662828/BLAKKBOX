"""
axis/report.py

Axis analysis reporting.
"""

from __future__ import annotations

from core.logger import (
    section,
    kv,
)

from configs.config import MAX_REPORT_CANDIDATES


class AxisReport:
    """
    Report axis analysis statistics.
    """

    def print(self, candidates: list[dict]) -> dict:

        total = len(candidates)

        valid = sum(
            1
            for candidate in candidates
            if candidate.get("valid", False)
        )

        rejected = total - valid

        average_score = (
            sum(
                candidate.get("score", 0)
                for candidate in candidates
            ) / total
            if total
            else 0.0
        )

        summary = {
            "total": total,
            "valid": valid,
            "rejected": rejected,
            "average_score": average_score,
        }

        section("AXIS ANALYSIS")

        kv("Candidates", summary["total"])
        kv("Valid Axis", summary["valid"])
        kv("Rejected", summary["rejected"])
        kv(
            "Average Score",
            f"{summary['average_score']:.1f}"
        )

        if total:

            section("TOP AXIS CANDIDATES")

            ranked = sorted(
                candidates,
                key=lambda candidate: candidate.get(
                    "score",
                    0
                ),
                reverse=True,
            )

            for index, candidate in enumerate(
                ranked[:MAX_REPORT_CANDIDATES],
                start=1,
            ):

                region = candidate.get("region")

                start = getattr(region, "start", 0)
                end = getattr(region, "end", 0)

                kv(
                    f"#{index}",
                    (
                        f"0x{start:08X} - "
                        f"0x{end:08X} | "
                        f"Score={candidate.get('score', 0)} | "
                        f"Valid={candidate.get('valid', False)}"
                    ),
                )

        return summary
