"""
axis/step_analyzer.py

Generic step statistics.
"""

from __future__ import annotations

from statistics import mean
from typing import Sequence


class StepAnalyzer:

    def analyze(
        self,
        values: Sequence[int],
    ) -> dict[str, float]:

        if len(values) < 2:
            return {
                "average_step": 0.0,
                "minimum_step": 0.0,
                "maximum_step": 0.0,
            }

        steps = [
            b - a
            for a, b in zip(values[:-1], values[1:])
        ]

        return {
            "average_step": float(mean(steps)),
            "minimum_step": float(min(steps)),
            "maximum_step": float(max(steps)),
        }
