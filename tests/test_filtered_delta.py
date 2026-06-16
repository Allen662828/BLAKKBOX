from types import SimpleNamespace

from delta.filtered_delta import DeltaFilter


def test_filtered_delta_keeps_small_delta():
    original = bytes([10, 20, 30])
    modified = bytes([10, 24, 30])
    region = SimpleNamespace(start=1, end=1)

    result = DeltaFilter().apply(original, modified, [region])

    assert result.values == {1: 24}
    assert result.summary()["small_deltas_kept"] == 1


def test_filtered_delta_reduces_medium_delta():
    original = bytes([10])
    modified = bytes([17])  # delta +7 => +6 after 80% rounding
    region = SimpleNamespace(start=0, end=0)

    result = DeltaFilter().apply(original, modified, [region])

    assert result.values == {0: 16}
    assert result.summary()["medium_deltas_reduced"] == 1


def test_filtered_delta_reduces_large_delta():
    original = bytes([100])
    modified = bytes([120])  # delta +20 => +11 after 55%
    region = SimpleNamespace(start=0, end=0)

    result = DeltaFilter().apply(original, modified, [region])

    assert result.values == {0: 111}
    assert result.summary()["large_deltas_reduced"] == 1


def test_filtered_delta_skips_mod_zero():
    original = bytes([55])
    modified = bytes([0])
    region = SimpleNamespace(start=0, end=0)

    result = DeltaFilter().apply(original, modified, [region])

    assert result.values == {}
    assert result.summary()["mod_zero_offsets_skipped"] == 1
