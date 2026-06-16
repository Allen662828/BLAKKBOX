from __future__ import annotations

from dataclasses import dataclass

from studio.calibration.axis import Axis
from studio.calibration.map import CalibrationMap


@dataclass(slots=True)
class CalibrationTable:
    """
    Complete calibration table consisting of:

        X Axis
        Y Axis
        Calibration Map
    """

    name: str

    x_axis: Axis

    y_axis: Axis

    calibration_map: CalibrationMap

    category: str = "Unknown"

    description: str = ""

    confidence: float = 0.0

    def contains(
        self,
        address: int,
    ) -> bool:

        return (
            self.x_axis.contains(address)
            or self.y_axis.contains(address)
            or self.calibration_map.contains(address)
        )

    @property
    def start_address(self) -> int:

        return min(
            self.x_axis.address,
            self.y_axis.address,
            self.calibration_map.address,
        )

    @property
    def end_address(self) -> int:

        return max(
            self.x_axis.end_address,
            self.y_axis.end_address,
            self.calibration_map.end_address,
        )

    @property
    def total_size(self) -> int:

        return (
            self.x_axis.size_bytes
            + self.y_axis.size_bytes
            + self.calibration_map.size_bytes
        )

    @property
    def rows(self) -> int:

        return self.calibration_map.rows

    @property
    def columns(self) -> int:

        return self.calibration_map.columns

    @property
    def modified(self) -> bool:

        return self.calibration_map.modified

    def summary(self) -> str:

        return (
            f"{self.name}\n"
            f"Category      : {self.category}\n"
            f"Address Range : "
            f"0x{self.start_address:08X} - "
            f"0x{self.end_address:08X}\n"
            f"Rows          : {self.rows}\n"
            f"Columns       : {self.columns}\n"
            f"Total Size    : {self.total_size} bytes\n"
            f"Modified      : {self.modified}\n"
            f"Confidence    : {self.confidence:.2f}"
        )

    def __str__(self):

        return self.summary()
