from __future__ import annotations

from pathlib import Path


class ProjectService:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def folders(self) -> list[Path]:
        if not self.root.exists():
            return []

        items = [
            path
            for path in self.root.iterdir()
            if path.is_dir()
            and not path.name.startswith(".")
            and path.name != "__pycache__"
        ]

        return sorted(items, key=lambda path: path.name.lower())

    def files(self, folder: Path) -> list[Path]:
        if not folder.exists():
            return []

        items = [
            path
            for path in folder.iterdir()
            if path.is_file()
            and not path.name.startswith(".")
            and path.name != "__pycache__"
        ]

        return sorted(items, key=lambda path: path.name.lower())
