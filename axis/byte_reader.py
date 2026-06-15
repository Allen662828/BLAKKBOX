"""
axis/byte_reader.py

Generic binary reader.
"""

from __future__ import annotations

from typing import Optional


class ByteReader:

    def __init__(self, data: bytes):
        self.data = data

    def u8(self, offset: int) -> Optional[int]:

        if offset < 0 or offset >= len(self.data):
            return None

        return self.data[offset]

    def u16_le(self, offset: int) -> Optional[int]:

        if offset < 0 or offset + 1 >= len(self.data):
            return None

        return int.from_bytes(
            self.data[offset:offset + 2],
            "little",
        )

    def u16_be(self, offset: int) -> Optional[int]:

        if offset < 0 or offset + 1 >= len(self.data):
            return None

        return int.from_bytes(
            self.data[offset:offset + 2],
            "big",
        )

    def slice(self, offset: int, length: int) -> bytes:

        if offset < 0:
            return b""

        return self.data[offset:offset + length]

    def size(self) -> int:
        return len(self.data)
