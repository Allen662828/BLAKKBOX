"""
tests/test_merger.py
"""

from delta.merger import DeltaMerger
from delta.region import DeltaRegion


def test_empty():

    merger = DeltaMerger()

    assert merger.merge([]) == []


def test_merge_adjacent():

    merger = DeltaMerger(max_gap=8)

    regions = [
        DeltaRegion(100, 120),
        DeltaRegion(125, 140),
    ]

    merged = merger.merge(regions)

    assert len(merged) == 1
    assert merged[0].start == 100
    assert merged[0].end == 140


def test_do_not_merge():

    merger = DeltaMerger(max_gap=4)

    regions = [
        DeltaRegion(100, 120),
        DeltaRegion(140, 160),
    ]

    merged = merger.merge(regions)

    assert len(merged) == 2


def test_sorted():

    merger = DeltaMerger()

    regions = [
        DeltaRegion(400, 450),
        DeltaRegion(100, 150),
        DeltaRegion(200, 250),
    ]

    merged = merger.merge(regions)

    assert merged[0].start == 100
