"""Final ROM merge logic.

The only valid final binary is:

    ENHANCED_BIN = ORIGINAL_BIN + FILTERED_DELTA

This module never copies the MOD file wholesale.
"""

from __future__ import annotations

from pathlib import Path


class FinalMerge:
    def merge(self, original: bytes, filtered_values: dict[int, int]) -> bytes:
        final = bytearray(original)

        for offset, value in filtered_values.items():
            if offset < 0 or offset >= len(final):
                raise ValueError(f"Filtered delta offset out of range: {offset}")
            if not 0 <= value <= 255:
                raise ValueError(f"Filtered delta value is not a byte: {value}")
            final[offset] = value

        return bytes(final)

    def export(self, final: bytes, output_file: str | Path) -> Path:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(final)
        return path
