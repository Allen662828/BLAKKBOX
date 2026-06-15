"""
axis/duplicate_analyzer.py

Generic duplicate statistics.
"""

from __future__ import annotations


class DuplicateAnalyzer:

    def analyze(
        self,
        values: list[int],
    ) -> dict[str, float]:

        total = len(values)

        if total == 0:
            return {
                "duplicate_ratio": 0.0,
                "unique_ratio": 0.0,
            }

        unique = len(set(values))

        return {
            "duplicate_ratio": 1.0 - (unique / total),
            "unique_ratio": unique / total,
        }
