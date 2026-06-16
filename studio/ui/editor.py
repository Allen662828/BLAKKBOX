from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit, QTabWidget


class Editor(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setDocumentMode(True)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index: int):
        widget = self.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.removeTab(index)

    def open_file(self, path: str | Path):
        file_path = Path(path)

        for index in range(self.count()):
            widget = self.widget(index)
            if widget is not None and widget.property("filepath") == str(file_path):
                self.setCurrentIndex(index)
                return

        editor = QPlainTextEdit()
        editor.setFont(QFont("Consolas", 10))
        editor.setProperty("filepath", str(file_path))
        editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            text = f"Failed to open {file_path}\n\n{exc}"

        editor.setPlainText(text)

        self.addTab(editor, file_path.name)
        self.setCurrentWidget(editor)
