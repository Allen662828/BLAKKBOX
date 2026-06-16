from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CalibrationMap:
    """
    Generic calibration map.
    """

    name: str
    address: int

    rows: int
    columns: int

    element_size: int

    x_axis: list[int] = field(default_factory=list)
    y_axis: list[int] = field(default_factory=list)
    values: list[list[int]] = field(default_factory=list)

    category: str = "Unknown"

    confidence: float = 0.0

    modified: bool = False

    description: str = ""

    @property
    def end_address(self) -> int:

        return (
            self.address
            + (self.rows * self.columns * self.element_size)
            - 1
        )

    @property
    def cell_count(self) -> int:

        return self.rows * self.columns

    @property
    def size_bytes(self) -> int:

        return (
            self.rows
            * self.columns
            * self.element_size
        )

    def contains(
        self,
        address: int,
    ) -> bool:

        return (
            self.address
            <= address
            <= self.end_address
        )

    def set_modified(
        self,
        value: bool = True,
    ):

        self.modified = value

    def value(
        self,
        row: int,
        column: int,
    ) -> int:

        return self.values[row][column]

    def set_value(
        self,
        row: int,
        column: int,
        value: int,
    ):

        self.values[row][column] = value

    def flatten(self) -> list[int]:

        result = []

        for row in self.values:
            result.extend(row)

        return result

    def summary(self) -> str:

        return (
            f"{self.name}\n"
            f"Category : {self.category}\n"
            f"Address  : 0x{self.address:08X}\n"
            f"Rows     : {self.rows}\n"
            f"Columns  : {self.columns}\n"
            f"Cells    : {self.cell_count}\n"
            f"Bytes    : {self.size_bytes}\n"
            f"Modified : {self.modified}\n"
            f"Confidence : {self.confidence:.2f}"
        )

    def __str__(self):

        return self.summary()
