from __future__ import annotations

from pathlib import Path

from studio.core.delta_engine import DeltaEngine, DeltaResult


class AnalysisService:
    def __init__(self):
        self.result: DeltaResult | None = None

    def analyze(
        self,
        original: str | Path,
        modified: str | Path,
    ) -> DeltaResult:

        self.result = DeltaEngine.compare(
            original,
            modified,
        )

        return self.result

    @property
    def has_result(self) -> bool:
        return self.result is not None

    @property
    def statistics(self):
        if self.result is None:
            return None

        return self.result.statistics

    @property
    def regions(self):
        if self.result is None:
            return []

        return self.result.regions

    @property
    def differences(self):
        if self.result is None:
            return []

        return self.result.differences

    def summary(self) -> str:

        if self.result is None:
            return "No analysis available."

        return DeltaEngine.summary(self.result)

    def clear(self):

        self.result = None
