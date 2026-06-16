from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem

from studio.core.region import Region


class DeltaRegions(QTableWidget):

    regionSelected = Signal(int)

    def __init__(self):
        super().__init__()

        self.setColumnCount(4)

        self.setHorizontalHeaderLabels(
            [
                "Start",
                "End",
                "Length",
                "Bytes",
            ]
        )

        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.cellDoubleClicked.connect(
            self._double_clicked
        )

        self._regions: list[Region] = []

    def load_regions(
        self,
        regions: list[Region],
    ):

        self.clearContents()

        self._regions = regions

        self.setRowCount(len(regions))

        for row, region in enumerate(regions):

            self.setItem(
                row,
                0,
                QTableWidgetItem(region.start_hex),
            )

            self.setItem(
                row,
                1,
                QTableWidgetItem(region.end_hex),
            )

            self.setItem(
                row,
                2,
                QTableWidgetItem(str(region.length)),
            )

            self.setItem(
                row,
                3,
                QTableWidgetItem(str(region.modified_bytes)),
            )

        self.resizeColumnsToContents()

    def _double_clicked(
        self,
        row,
        column,
    ):

        if row >= len(self._regions):
            return

        self.regionSelected.emit(
            self._regions[row].start
        )
