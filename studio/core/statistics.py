from __future__ import annotations

from dataclasses import dataclass

from studio.core.region import Region


@dataclass(slots=True)
class DeltaStatistics:
    file_size: int
    modified_bytes: int
    modified_regions: int
    largest_region: int
    percentage_modified: float

    @property
    def unmodified_bytes(self) -> int:
        return self.file_size - self.modified_bytes

    def __str__(self) -> str:
        return (
            f"File Size: {self.file_size:,} bytes\n"
            f"Modified Bytes: {self.modified_bytes:,}\n"
            f"Modified Regions: {self.modified_regions:,}\n"
            f"Largest Region: {self.largest_region:,} bytes\n"
            f"Modified: {self.percentage_modified:.4f}%"
        )


class Statistics:
    @staticmethod
    def calculate(
        file_size: int,
        regions: list[Region],
    ) -> DeltaStatistics:

        modified_bytes = sum(
            region.modified_bytes
            for region in regions
        )

        largest_region = max(
            (region.length for region in regions),
            default=0,
        )

        percentage = (
            (modified_bytes / file_size) * 100.0
            if file_size > 0
            else 0.0
        )

        return DeltaStatistics(
            file_size=file_size,
            modified_bytes=modified_bytes,
            modified_regions=len(regions),
            largest_region=largest_region,
            percentage_modified=percentage,
        )
