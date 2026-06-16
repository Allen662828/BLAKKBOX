from __future__ import annotations

from dataclasses import dataclass
from hashlib import md5, sha256
from pathlib import Path


@dataclass(slots=True)
class BinFile:
    path: Path
    data: bytes
    size: int
    md5: str
    sha256: str


class BinLoader:
    @staticmethod
    def load(path: str | Path) -> BinFile:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        data = path.read_bytes()

        return BinFile(
            path=path,
            data=data,
            size=len(data),
            md5=md5(data).hexdigest(),
            sha256=sha256(data).hexdigest(),
        )

    @staticmethod
    def save(path: str | Path, data: bytes) -> None:
        Path(path).write_bytes(data)

    @staticmethod
    def compare(first: BinFile, second: BinFile) -> bool:
        return first.data == second.data

    @staticmethod
    def difference_count(first: BinFile, second: BinFile) -> int:
        length = min(first.size, second.size)

        diff = sum(
            1
            for i in range(length)
            if first.data[i] != second.data[i]
        )

        diff += abs(first.size - second.size)

        return diff

    @staticmethod
    def verify_same_size(first: BinFile, second: BinFile) -> bool:
        return first.size == second.size
