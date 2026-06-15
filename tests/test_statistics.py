"""
tests/test_statistics.py
"""

from analysis.statistics import (
    StatisticsAnalyzer,
)


def test_statistics():

    data = bytes([
        0,
        1,
        2,
        3,
        4,
        5,
        5,
        5,
    ])

    analyzer = StatisticsAnalyzer()

    stats = analyzer.analyze(data)

    assert stats.file_size == 8
    assert stats.zero_bytes == 1
    assert stats.non_zero_bytes == 7
    assert stats.unique_values == 6
    assert stats.minimum == 0
    assert stats.maximum == 5


def test_empty():

    analyzer = StatisticsAnalyzer()

    stats = analyzer.analyze(b"")

    assert stats.file_size == 0
    assert stats.zero_bytes == 0
    assert stats.unique_values == 0
