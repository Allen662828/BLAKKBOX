"""
axis/range_analyzer.py

Generic range statistics.
"""

from __future__ import annotations


class RangeAnalyzer:

    def analyze(
        self,
        values: list[int],
    ) -> dict[str, int]:

        if not values:
            return {
                "minimum": 0,
                "maximum": 0,
                "span": 0,
            }

        minimum = min(values)
        maximum = max(values)

        return {
            "minimum": minimum,
            "maximum": maximum,
            "span": maximum - minimum,
        }
