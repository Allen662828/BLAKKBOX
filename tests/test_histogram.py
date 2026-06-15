"""
tests/test_histogram.py
"""

from analysis.histogram import (
    HistogramAnalyzer,
)


def test_empty_histogram() -> None:

    analyzer = HistogramAnalyzer()

    histogram = analyzer.analyze(b"")

    assert histogram.unique_values == 0
    assert histogram.most_common == 0
    assert histogram.least_common == 0

    assert len(histogram.frequencies) == 256
    assert len(histogram.percentages) == 256


def test_simple_histogram() -> None:

    analyzer = HistogramAnalyzer()

    histogram = analyzer.analyze(
        bytes([0, 1, 1, 2, 2, 2])
    )

    assert histogram.frequencies[0] == 1
    assert histogram.frequencies[1] == 2
    assert histogram.frequencies[2] == 3

    assert histogram.unique_values == 3

    assert histogram.most_common == 2
    assert histogram.least_common == 0


def test_all_byte_values() -> None:

    analyzer = HistogramAnalyzer()

    histogram = analyzer.analyze(
        bytes(range(256))
    )

    assert histogram.unique_values == 256

    assert sum(histogram.frequencies) == 256
