from PySide6.QtWidgets import QPlainTextEdit


class OutputConsole(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.setReadOnly(True)
        self.appendPlainText("BLAKKBOX Studio started.")

    def info(self, message: str):
        self.appendPlainText(message)

    def warning(self, message: str):
        self.appendPlainText(f"WARNING: {message}")

    def error(self, message: str):
        self.appendPlainText(f"ERROR: {message}")
