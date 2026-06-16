from __future__ import annotations

from pathlib import Path

from studio.core.delta_engine import DeltaEngine, DeltaResult
from studio.engine.delta_logic import (
    DeltaLogic,
    FilteredDifference,
)


class CalibrationEngine:
    """
    BLAKKBOX Calibration Engine

    FINAL = ORIGINAL + FILTERED_DELTA
    """

    def __init__(self):

        self.result: DeltaResult | None = None
        self.filtered: list[FilteredDifference] = []

    def analyze(
        self,
        original: str | Path,
        modified: str | Path,
    ) -> DeltaResult:

        self.result = DeltaEngine.compare(
            original,
            modified,
        )

        self.filtered = DeltaLogic.apply(
            self.result.differences
        )

        return self.result

    def build_final(
        self,
        original: str | Path,
    ) -> bytes:

        if self.result is None:
            raise RuntimeError(
                "Analyze must be called first."
            )

        original_bytes = Path(original).read_bytes()

        return DeltaLogic.build_final_bin(
            original_bytes,
            self.filtered,
        )

    def save(
        self,
        original: str | Path,
        output: str | Path,
    ):

        data = self.build_final(original)

        Path(output).write_bytes(data)

    @property
    def modified_regions(self):

        if self.result is None:
            return []

        return self.result.regions

    @property
    def statistics(self):

        if self.result is None:
            return None

        return self.result.statistics

    @property
    def modified_bytes(self):

        if self.result is None:
            return 0

        return len(self.result.differences)

    @property
    def filtered_bytes(self):

        return len(self.filtered)

    def summary(self):

        if self.result is None:
            return "No analysis."

        return (
            f"{self.modified_bytes:,} modified bytes\n"
            f"{len(self.modified_regions)} regions\n"
            f"{self.filtered_bytes:,} filtered bytes\n"
            f"{self.statistics.percentage_modified:.4f}% modified"
        )
