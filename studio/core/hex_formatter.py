from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class HexLine:
    offset: int
    hex_text: str
    ascii_text: str


class HexFormatter:
    BYTES_PER_ROW = 16

    @staticmethod
    def format_bytes(data: bytes) -> list[HexLine]:
        lines: list[HexLine] = []

        for offset in range(0, len(data), HexFormatter.BYTES_PER_ROW):
            chunk = data[offset : offset + HexFormatter.BYTES_PER_ROW]

            hex_text = " ".join(f"{byte:02X}" for byte in chunk)
            ascii_text = "".join(
                chr(byte) if 32 <= byte <= 126 else "."
                for byte in chunk
            )

            lines.append(
                HexLine(
                    offset=offset,
                    hex_text=hex_text,
                    ascii_text=ascii_text,
                )
            )

        return lines

    @staticmethod
    def format_path(path: str | Path) -> list[HexLine]:
        file_path = Path(path)
        data = file_path.read_bytes()
        return HexFormatter.format_bytes(data)
