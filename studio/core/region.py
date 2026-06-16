from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Region:
    start: int
    end: int
    length: int
    modified_bytes: int

    @property
    def start_hex(self) -> str:
        return f"0x{self.start:08X}"

    @property
    def end_hex(self) -> str:
        return f"0x{self.end:08X}"

    def contains(self, offset: int) -> bool:
        return self.start <= offset <= self.end

    def to_dict(self) -> dict:
        return {
            "start": self.start,
            "end": self.end,
            "length": self.length,
            "modified_bytes": self.modified_bytes,
            "start_hex": self.start_hex,
            "end_hex": self.end_hex,
        }

    def __str__(self) -> str:
        return (
            f"{self.start_hex} - "
            f"{self.end_hex} "
            f"({self.length} bytes)"
        )
