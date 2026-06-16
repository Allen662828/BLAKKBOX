from __future__ import annotations

from pathlib import Path

from studio.core.delta_engine import DeltaEngine, DeltaResult
from studio.services.analysis_service import AnalysisService


class AnalysisEngine:
    """
    Main analysis entry point for BLAKKBOX Studio.

    Pipeline

    ORIGINAL.bin
          │
          ▼
    DeltaEngine
          │
          ▼
    Region Detection
          │
          ▼
    Map Detection (next stage)
          │
          ▼
    Classification (next stage)
          │
          ▼
    Delta Logic (next stage)
    """

    def __init__(self):

        self.analysis = AnalysisService()

    def analyze(
        self,
        original: str | Path,
        modified: str | Path,
    ) -> DeltaResult:

        return self.analysis.analyze(
            original,
            modified,
        )

    def summary(self) -> str:

        return self.analysis.summary()

    @property
    def statistics(self):

        return self.analysis.statistics

    @property
    def regions(self):

        return self.analysis.regions

    @property
    def differences(self):

        return self.analysis.differences

    @property
    def has_result(self):

        return self.analysis.has_result

    def clear(self):

        self.analysis.clear()
