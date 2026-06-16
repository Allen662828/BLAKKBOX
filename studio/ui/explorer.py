from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from studio.services.project_service import ProjectService


class Explorer(QTreeWidget):
    fileOpened = Signal(Path)

    def __init__(self, project: ProjectService):
        super().__init__()

        self.project = project
        self.setHeaderHidden(True)
        self.itemDoubleClicked.connect(self._double_clicked)

        self.refresh()

    def refresh(self):
        self.clear()

        root = QTreeWidgetItem([self.project.root.name])
        root.setData(0, Qt.ItemDataRole.UserRole, str(self.project.root))
        self.addTopLevelItem(root)

        self._populate(root, self.project.root)
        root.setExpanded(True)

    def _populate(self, parent: QTreeWidgetItem, folder: Path):
        try:
            children = sorted(
                [
                    path
                    for path in folder.iterdir()
                    if not path.name.startswith(".")
                    and path.name != "__pycache__"
                ],
                key=lambda path: (not path.is_dir(), path.name.lower()),
            )
        except Exception:
            return

        for child in children:
            item = QTreeWidgetItem([child.name])
            item.setData(0, Qt.ItemDataRole.UserRole, str(child))
            parent.addChild(item)

            if child.is_dir():
                self._populate(item, child)

    def _double_clicked(self, item: QTreeWidgetItem, column: int):
        path_value = item.data(0, Qt.ItemDataRole.UserRole)
        if not path_value:
            return

        path = Path(path_value)
        if path.is_file():
            self.fileOpened.emit(path)
