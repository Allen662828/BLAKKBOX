"""
analysis/statistics.py

Generic binary statistics.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median, pstdev


@dataclass(slots=True)
class BinaryStatistics:

    file_size: int

    zero_bytes: int
    non_zero_bytes: int

    unique_values: int

    minimum: int
    maximum: int

    mean: float
    median: float
    std_dev: float


class StatisticsAnalyzer:
    """
    Generic binary statistics analyzer.
    """

    def analyze(
        self,
        data: bytes,
    ) -> BinaryStatistics:

        if not data:

            return BinaryStatistics(
                file_size=0,
                zero_bytes=0,
                non_zero_bytes=0,
                unique_values=0,
                minimum=0,
                maximum=0,
                mean=0.0,
                median=0.0,
                std_dev=0.0,
            )

        values = list(data)

        zero_bytes = values.count(0)

        return BinaryStatistics(
            file_size=len(values),

            zero_bytes=zero_bytes,
            non_zero_bytes=len(values) - zero_bytes,

            unique_values=len(set(values)),

            minimum=min(values),
            maximum=max(values),

            mean=float(mean(values)),
            median=float(median(values)),
            std_dev=float(pstdev(values)),
        )
