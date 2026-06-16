from __future__ import annotations

from pathlib import Path

from studio.core.bin_loader import BinLoader, BinFile


class FileService:
    def __init__(self):
        self.current: BinFile | None = None

    def open(self, path: str | Path) -> BinFile:
        self.current = BinLoader.load(path)
        return self.current

    def close(self):
        self.current = None

    @property
    def is_open(self) -> bool:
        return self.current is not None

    @property
    def filename(self) -> str:
        if self.current is None:
            return ""
        return self.current.path.name

    @property
    def path(self) -> Path | None:
        if self.current is None:
            return None
        return self.current.path

    @property
    def data(self) -> bytes:
        if self.current is None:
            return b""
        return self.current.data

    @property
    def size(self) -> int:
        if self.current is None:
            return 0
        return self.current.size

    @property
    def md5(self) -> str:
        if self.current is None:
            return ""
        return self.current.md5

    @property
    def sha256(self) -> str:
        if self.current is None:
            return ""
        return self.current.sha256

    def reload(self):
        if self.current is None:
            return

        self.current = BinLoader.load(self.current.path)
