from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Axis:
    """
    Generic calibration axis.
    """

    name: str

    address: int

    length: int

    element_size: int

    values: list[int] = field(default_factory=list)

    units: str = ""

    description: str = ""

    confidence: float = 0.0

    @property
    def end_address(self) -> int:

        return (
            self.address
            + (self.length * self.element_size)
            - 1
        )

    @property
    def size_bytes(self) -> int:

        return self.length * self.element_size

    def contains(
        self,
        address: int,
    ) -> bool:

        return (
            self.address
            <= address
            <= self.end_address
        )

    def is_monotonic(self) -> bool:

        if len(self.values) < 2:
            return True

        return all(
            self.values[i] <= self.values[i + 1]
            for i in range(len(self.values) - 1)
        )

    def minimum(self) -> int:

        if not self.values:
            return 0

        return min(self.values)

    def maximum(self) -> int:

        if not self.values:
            return 0

        return max(self.values)

    def summary(self) -> str:

        return (
            f"{self.name}\n"
            f"Address    : 0x{self.address:08X}\n"
            f"Length     : {self.length}\n"
            f"Element    : {self.element_size} bytes\n"
            f"Size       : {self.size_bytes} bytes\n"
            f"Units      : {self.units}\n"
            f"Min        : {self.minimum()}\n"
            f"Max        : {self.maximum()}\n"
            f"Monotonic  : {self.is_monotonic()}\n"
            f"Confidence : {self.confidence:.2f}"
        )

    def __str__(self):

        return self.summary()
