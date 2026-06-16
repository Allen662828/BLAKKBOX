from PySide6.QtWidgets import QLabel, QStatusBar


class StudioStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

        self.state = QLabel("Ready")
        self.branch = QLabel("develop")

        self.addWidget(self.state)
        self.addPermanentWidget(self.branch)

    def set_state(self, text: str):
        self.state.setText(text)

    def set_branch(self, branch: str):
        self.branch.setText(branch)
