"""
geometry/rectangle.py
"""

from __future__ import annotations


class RectangleDetector:

    def analyze(self, shape: tuple[int, int]) -> bool:

        rows, cols = shape

        return rows >= 2 and cols >= 2

    def detect(self, size: int) -> tuple[int, int]:

        if size <= 0:
            return (0, 0)

        best = (1, size)

        for rows in range(2, int(size**0.5) + 1):

            if size % rows == 0:
                best = (rows, size // rows)

        return best


# ------------------------------------------------------------------
# Backward compatibility
# ------------------------------------------------------------------

RectangleAnalyzer = RectangleDetector
