"""
delta/merger.py

Merge adjacent delta regions into larger logical regions.

A region is merged when the byte gap between consecutive
regions is <= max_gap.

Example

Region A : 0x1000 - 0x1040
Gap      : 3 bytes
Region B : 0x1044 - 0x1080

Result

Region : 0x1000 - 0x1080
"""

from delta.region import DeltaRegion


class DeltaMerger:

    def __init__(self, max_gap: int = 8):
        self.max_gap = max_gap

    def merge(self, regions):

        if not regions:
            return []

        # Ensure regions are sorted
        regions = sorted(regions, key=lambda r: r.start)

        merged = []

        current = DeltaRegion(
            start=regions[0].start,
            end=regions[0].end
        )

        for region in regions[1:]:

            gap = region.start - current.end - 1

            if gap <= self.max_gap:
                # Extend current region
                current.end = max(current.end, region.end)
            else:
                merged.append(current)

                current = DeltaRegion(
                    start=region.start,
                    end=region.end
                )

        merged.append(current)

        return merged

    def statistics(self, before, after):

        print()
        print("=" * 60)
        print("REGION MERGER")
        print("=" * 60)

        print(f"Original Regions : {len(before)}")
        print(f"Merged Regions   : {len(after)}")
        print(f"Reduction        : {len(before) - len(after)}")

        if len(before):
            reduction = (
                (len(before) - len(after))
                / len(before)
            ) * 100

            print(f"Reduction %      : {reduction:.1f}%")

        print("=" * 60)