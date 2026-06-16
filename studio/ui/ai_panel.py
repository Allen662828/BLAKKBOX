from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class AIPanel(QWidget):
    promptSubmitted = Signal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.prompt = QTextEdit()
        self.prompt.setPlaceholderText("Ask BLAKKBOX AI...")
        self.prompt.setMaximumHeight(100)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self._send_prompt)

        layout.addWidget(self.chat)
        layout.addWidget(self.prompt)
        layout.addWidget(self.send_button)

    def _send_prompt(self):
        text = self.prompt.toPlainText().strip()
        if not text:
            return

        self.chat.append(f"You: {text}")
        self.prompt.clear()
        self.promptSubmitted.emit(text)

    def append_response(self, text: str):
        self.chat.append(f"AI: {text}")
