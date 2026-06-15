"""
analysis/histogram.py

Generic byte histogram analysis.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(slots=True)
class Histogram:
    """
    Byte frequency statistics.
    """

    frequencies: list[int]
    percentages: list[float]

    unique_values: int

    most_common: int
    least_common: int


class HistogramAnalyzer:
    """
    Analyze byte frequency distribution.
    """

    def analyze(
        self,
        data: bytes,
    ) -> Histogram:

        frequencies = [0] * 256

        if not data:

            return Histogram(
                frequencies=frequencies,
                percentages=[0.0] * 256,
                unique_values=0,
                most_common=0,
                least_common=0,
            )

        counter = Counter(data)

        for value, count in counter.items():
            frequencies[value] = count

        total = len(data)

        percentages = [
            (count / total) * 100.0
            for count in frequencies
        ]

        unique_values = len(counter)

        most_common = max(
            counter.items(),
            key=lambda item: item[1],
        )[0]

        least_common = min(
            counter.items(),
            key=lambda item: item[1],
        )[0]

        return Histogram(
            frequencies=frequencies,
            percentages=percentages,
            unique_values=unique_values,
            most_common=most_common,
            least_common=least_common,
        )
