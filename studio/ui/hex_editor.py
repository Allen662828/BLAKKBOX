from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit

from studio.core.hex_formatter import HexFormatter


class HexEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setFont(QFont("Consolas", 10))

        self.file_path: Path | None = None
        self.raw_data: bytes = b""

    def clear_file(self):
        self.file_path = None
        self.raw_data = b""
        self.clear()

    def open_bytes(self, data: bytes):
        self.raw_data = data

        lines = []

        for line in HexFormatter.format_bytes(data):

            lines.append(
                f"{line.offset:08X}  "
                f"{line.hex_text:<47}  "
                f"{line.ascii_text}"
            )

        self.setPlainText("\n".join(lines))

    def open_file(self, path: str | Path):

        self.file_path = Path(path)

        self.raw_data = self.file_path.read_bytes()

        self.open_bytes(self.raw_data)

    @property
    def size(self) -> int:
        return len(self.raw_data)

    @property
    def filename(self) -> str:
        if self.file_path is None:
            return ""

        return self.file_path.name
