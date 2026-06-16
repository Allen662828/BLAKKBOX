from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class CompareDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Compare BIN Files")
        self.resize(700, 180)

        self.original_edit = QLineEdit()
        self.modified_edit = QLineEdit()

        original_button = QPushButton("Browse...")
        modified_button = QPushButton("Browse...")

        original_button.clicked.connect(self._browse_original)
        modified_button.clicked.connect(self._browse_modified)

        form = QFormLayout()

        original_layout = QHBoxLayout()
        original_layout.addWidget(self.original_edit)
        original_layout.addWidget(original_button)

        modified_layout = QHBoxLayout()
        modified_layout.addWidget(self.modified_edit)
        modified_layout.addWidget(modified_button)

        form.addRow("Original BIN", original_layout)
        form.addRow("Modified BIN", modified_layout)

        ok_button = QPushButton("Analyze")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addStretch()
        layout.addLayout(buttons)

    def _browse_original(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select ORIGINAL BIN",
            "",
            "Binary Files (*.bin *.rom *.hex *.ori *.mod);;All Files (*.*)",
        )

        if filename:
            self.original_edit.setText(filename)

    def _browse_modified(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select MODIFIED BIN",
            "",
            "Binary Files (*.bin *.rom *.hex *.ori *.mod);;All Files (*.*)",
        )

        if filename:
            self.modified_edit.setText(filename)

    @property
    def original_path(self) -> Path | None:

        text = self.original_edit.text().strip()

        if not text:
            return None

        return Path(text)

    @property
    def modified_path(self) -> Path | None:

        text = self.modified_edit.text().strip()

        if not text:
            return None

        return Path(text)
