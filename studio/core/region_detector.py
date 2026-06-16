from __future__ import annotations

from studio.core.byte_compare import ByteDifference
from studio.core.region import Region


class RegionDetector:
    @staticmethod
    def detect(
        differences: list[ByteDifference],
    ) -> list[Region]:

        if not differences:
            return []

        regions: list[Region] = []

        start = differences[0].offset
        previous = differences[0].offset
        modified = 1

        for diff in differences[1:]:

            if diff.offset == previous + 1:
                previous = diff.offset
                modified += 1
                continue

            regions.append(
                Region(
                    start=start,
                    end=previous,
                    length=(previous - start) + 1,
                    modified_bytes=modified,
                )
            )

            start = diff.offset
            previous = diff.offset
            modified = 1

        regions.append(
            Region(
                start=start,
                end=previous,
                length=(previous - start) + 1,
                modified_bytes=modified,
            )
        )

        return regions

    @staticmethod
    def largest(
        regions: list[Region],
    ) -> Region | None:

        if not regions:
            return None

        return max(
            regions,
            key=lambda region: region.length,
        )

    @staticmethod
    def total_modified_bytes(
        regions: list[Region],
    ) -> int:

        return sum(
            region.modified_bytes
            for region in regions
        )
