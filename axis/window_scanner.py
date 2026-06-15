"""
axis/window_scanner.py

Generic sliding-window scanner.
"""

from __future__ import annotations

from typing import Iterator


class WindowScanner:

    def scan(
        self,
        data: bytes,
        window_size: int,
        step: int = 1,
    ) -> Iterator[tuple[int, bytes]]:

        if window_size <= 0:
            raise ValueError("window_size must be > 0")

        if step <= 0:
            raise ValueError("step must be > 0")

        limit = len(data) - window_size + 1

        for offset in range(0, max(limit, 0), step):
            yield offset, data[offset:offset + window_size]
