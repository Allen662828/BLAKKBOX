"""
tests/test_delta.py
"""

from delta.extractor import DeltaExtractor


def test_identical():

    original = bytes([1, 2, 3, 4])

    modified = bytes([1, 2, 3, 4])

    offsets = DeltaExtractor().extract(original, modified)

    assert offsets == []


def test_single_change():

    original = bytes([1, 2, 3])

    modified = bytes([1, 9, 3])

    offsets = DeltaExtractor().extract(original, modified)

    assert offsets == [1]
