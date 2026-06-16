from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFormLayout,
    QLabel,
    QWidget,
)

from studio.core.bin_loader import BinLoader


class FileInfo(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout(self)

        self.name = QLabel("-")
        self.location = QLabel("-")
        self.size = QLabel("-")
        self.md5 = QLabel("-")
        self.sha256 = QLabel("-")

        self.location.setWordWrap(True)
        self.md5.setWordWrap(True)
        self.sha256.setWordWrap(True)

        layout.addRow("Filename", self.name)
        layout.addRow("Location", self.location)
        layout.addRow("Size", self.size)
        layout.addRow("MD5", self.md5)
        layout.addRow("SHA256", self.sha256)

    def clear(self):
        self.name.setText("-")
        self.location.setText("-")
        self.size.setText("-")
        self.md5.setText("-")
        self.sha256.setText("-")

    def load(self, path: str | Path):

        info = BinLoader.load(path)

        self.name.setText(info.path.name)
        self.location.setText(str(info.path))
        self.size.setText(f"{info.size:,} bytes")
        self.md5.setText(info.md5)
        self.sha256.setText(info.sha256)
