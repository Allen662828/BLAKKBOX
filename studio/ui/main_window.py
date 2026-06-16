from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QDockWidget,
    QLabel,
    QMainWindow,
    QMessageBox,
    QToolBar,
)

from studio.services.file_service import FileService
from studio.services.project_service import ProjectService
from studio.ui.ai_panel import AIPanel
from studio.ui.editor import Editor
from studio.ui.explorer import Explorer
from studio.ui.file_info import FileInfo
from studio.ui.hex_editor import HexEditor
from studio.ui.output import OutputConsole
from studio.ui.statusbar import StudioStatusBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BLAKKBOX Studio")
        self.resize(1700, 950)

        self.setAcceptDrops(True)

        self.project = ProjectService(Path.cwd())
        self.file_service = FileService()

        self.editor = Editor()
        self.hex_editor = HexEditor()
        self.file_info = FileInfo()
        self.explorer = Explorer(self.project)
        self.output = OutputConsole()
        self.ai = AIPanel()
        self.status = StudioStatusBar()

        self._create_menu()
        self._create_toolbar()
        self._create_workspace()
        self._create_docks()

        self.setStatusBar(self.status)

        self.explorer.fileOpened.connect(self.open_source_file)
        self.ai.promptSubmitted.connect(self.ai_prompt)

        self.output.info("BLAKKBOX Studio initialized.")

    # --------------------------------------------------
    # Menu
    # --------------------------------------------------

    def _create_menu(self):

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        menu.addMenu("&Edit")
        menu.addMenu("&View")
        menu.addMenu("&Tools")
        menu.addMenu("&Git")
        menu.addMenu("&AI")
        menu.addMenu("&Help")

        open_bin = QAction("Open BIN...", self)
        open_bin.triggered.connect(self.open_bin)

        file_menu.addAction(open_bin)
        file_menu.addSeparator()
        file_menu.addAction(
            QAction(
                "Exit",
                self,
                triggered=self.close,
            )
        )

    # --------------------------------------------------
    # Toolbar
    # --------------------------------------------------

    def _create_toolbar(self):

        toolbar = QToolBar("Main")
        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        open_action = QAction("Open BIN", self)
        open_action.triggered.connect(self.open_bin)

        compare_action = QAction("Compare", self)
        compare_action.triggered.connect(
            lambda: self.output.info("Compare not implemented.")
        )

        analyze_action = QAction("Analyze", self)
        analyze_action.triggered.connect(
            lambda: self.output.info("Analyze not implemented.")
        )

        ai_action = QAction("AI", self)
        ai_action.triggered.connect(
            lambda: self.status.set_state("AI Ready")
        )

        toolbar.addAction(open_action)
        toolbar.addAction(compare_action)
        toolbar.addAction(analyze_action)
        toolbar.addAction(ai_action)

    # --------------------------------------------------
    # Workspace
    # --------------------------------------------------

    def _create_workspace(self):

        self.setCentralWidget(self.editor)

    # --------------------------------------------------
    # Docks
    # --------------------------------------------------

    def _create_docks(self):

        explorer = QDockWidget("Project Explorer", self)
        explorer.setWidget(self.explorer)
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            explorer,
        )

        info = QDockWidget("File Information", self)
        info.setWidget(self.file_info)
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            info,
        )

        output = QDockWidget("Output", self)
        output.setWidget(self.output)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            output,
        )

        ai = QDockWidget("AI Assistant", self)
        ai.setWidget(self.ai)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            ai,
        )

        hex_view = QDockWidget("HEX Viewer", self)
        hex_view.setWidget(self.hex_editor)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            hex_view,
        )

    # --------------------------------------------------
    # Explorer
    # --------------------------------------------------

    def open_source_file(self, path: Path):

        suffix = path.suffix.lower()

        if suffix in (
            ".bin",
            ".rom",
            ".hex",
            ".ori",
            ".mod",
        ):
            self.load_binary(path)
            return

        self.editor.open_file(path)

        self.output.info(f"Opened {path}")

        self.status.set_state(path.name)

    # --------------------------------------------------
    # BIN Loader
    # --------------------------------------------------

    def open_bin(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Binary",
            "",
            "Binary Files (*.bin *.rom *.hex *.ori *.mod);;All Files (*.*)",
        )

        if filename:
            self.load_binary(Path(filename))

    def load_binary(self, path: Path):

        try:

            self.file_service.open(path)

            self.hex_editor.open_bytes(
                self.file_service.data
            )

            self.file_info.load(path)

            self.output.info(
                f"Loaded BIN: {path.name}"
            )

            self.status.set_state(path.name)

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )

            self.output.error(str(exc))

    # --------------------------------------------------
    # AI
    # --------------------------------------------------

    def ai_prompt(self, prompt: str):

        self.output.info(f"AI > {prompt}")

        self.ai.append_response(
            "AI backend not connected yet."
        )

    # --------------------------------------------------
    # Drag & Drop
    # --------------------------------------------------

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):

        urls = event.mimeData().urls()

        if not urls:
            return

        path = Path(urls[0].toLocalFile())

        if path.is_file():
            self.open_source_file(path)
