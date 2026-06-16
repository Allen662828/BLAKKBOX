from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from studio.core.bin_loader import BinLoader


@dataclass(slots=True)
class ByteDifference:
    offset: int
    original: int
    modified: int


class ByteCompare:
    @staticmethod
    def compare_bytes(
        original: bytes,
        modified: bytes,
    ) -> list[ByteDifference]:

        length = min(len(original), len(modified))

        differences: list[ByteDifference] = []

        for offset in range(length):

            if original[offset] != modified[offset]:

                differences.append(
                    ByteDifference(
                        offset=offset,
                        original=original[offset],
                        modified=modified[offset],
                    )
                )

        return differences

    @staticmethod
    def compare_files(
        original_file: str | Path,
        modified_file: str | Path,
    ) -> list[ByteDifference]:

        original = BinLoader.load(original_file)
        modified = BinLoader.load(modified_file)

        if original.size != modified.size:
            raise ValueError(
                "Binary files must be the same size."
            )

        return ByteCompare.compare_bytes(
            original.data,
            modified.data,
        )

    @staticmethod
    def modified_byte_count(
        original_file: str | Path,
        modified_file: str | Path,
    ) -> int:

        return len(
            ByteCompare.compare_files(
                original_file,
                modified_file,
            )
        )

    @staticmethod
    def identical(
        original_file: str | Path,
        modified_file: str | Path,
    ) -> bool:

        return (
            ByteCompare.modified_byte_count(
                original_file,
                modified_file,
            )
            == 0
        )
