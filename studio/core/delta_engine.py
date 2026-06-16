from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from studio.core.bin_loader import BinLoader
from studio.core.byte_compare import ByteCompare, ByteDifference
from studio.core.region import Region
from studio.core.region_detector import RegionDetector
from studio.core.statistics import DeltaStatistics, Statistics


@dataclass(slots=True)
class DeltaResult:
    original_path: Path
    modified_path: Path

    original_size: int
    modified_size: int

    differences: list[ByteDifference]
    regions: list[Region]
    statistics: DeltaStatistics

    @property
    def identical(self) -> bool:
        return len(self.differences) == 0

    @property
    def modified_bytes(self) -> int:
        return len(self.differences)

    @property
    def modified_regions(self) -> int:
        return len(self.regions)


class DeltaEngine:
    @staticmethod
    def compare(
        original_file: str | Path,
        modified_file: str | Path,
    ) -> DeltaResult:

        original = BinLoader.load(original_file)
        modified = BinLoader.load(modified_file)

        if original.size != modified.size:
            raise ValueError(
                "Original and Modified BIN must be identical size."
            )

        differences = ByteCompare.compare_bytes(
            original.data,
            modified.data,
        )

        regions = RegionDetector.detect(
            differences,
        )

        statistics = Statistics.calculate(
            original.size,
            regions,
        )

        return DeltaResult(
            original_path=original.path,
            modified_path=modified.path,
            original_size=original.size,
            modified_size=modified.size,
            differences=differences,
            regions=regions,
            statistics=statistics,
        )

    @staticmethod
    def summary(result: DeltaResult) -> str:

        return (
            "========== Delta Analysis ==========\n"
            f"Original : {result.original_path.name}\n"
            f"Modified : {result.modified_path.name}\n"
            f"File Size: {result.original_size:,} bytes\n"
            f"Modified Bytes : {result.modified_bytes:,}\n"
            f"Modified Regions: {result.modified_regions:,}\n"
            f"Largest Region : {result.statistics.largest_region:,} bytes\n"
            f"Modified % : {result.statistics.percentage_modified:.4f}%\n"
            f"Identical : {result.identical}"
        )
